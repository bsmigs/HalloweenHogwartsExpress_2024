from sanic import Sanic
from sanic.response import html, json
import asyncio
from train import Train
import serial

app = Sanic("ButtonApp")

# serve static files from the 'static' directory
app.static('/static', './static')

# HTML content with buttons that make asynchronous requests
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hogwarts Page</title>
    <style>
        /* add margin to all images */
        img 
        {
            margin: 30px;
        }
    </style>
    <script>
        async function buttonAction(action) {
            const response = await fetch('/action/' + action);
            const result = await response.json();
            document.getElementById('result').innerHTML = result.message;
        }
    </script>
</head>
<body>
    <h1>Hogwarts Express Action Page</h1>
    
    <h2>Basic Controls</h2>
    <img src="/static/smoke.png" onclick="buttonAction('smoke')" style="cursor:pointer; width=100px; height=100px;" alt="Image 8"/>
    <img src="/static/lightbulb.jpg" onclick="buttonAction('lights')" style="cursor:pointer; width=100px; height=100px;" alt="Image 9"/>
    <img src="/static/horn.png" onclick="buttonAction('horn')" style="cursor:pointer; width=100px; height=100px;" alt="Image 10"/>
    <img src="/static/wheels.png" onclick="buttonAction('wheels')" style="cursor:pointer; width=100px; height=100px;" alt="Image 11"/>
    
    <h2>Music Controls</h2>
    <img src="/static/previous.png" onclick="buttonAction('previous')" style="cursor:pointer; width=100px;" alt="Image 1"/>
    <img src="/static/play.png" onclick="buttonAction('play')" style="cursor:pointer; width=100px;" alt="Image 2"/>
    <img src="/static/next.png" onclick="buttonAction('next')" style="cursor:pointer; width=100px;" alt="Image 3"/>
    <img src="/static/pause.png" onclick="buttonAction('pause')" style="cursor:pointer; width=100px;" alt="Image 4"/>
    <img src="/static/stop.png" onclick="buttonAction('stop')" style="cursor:pointer; width=100px;" alt="Image 5"/>
    <img src="/static/raise_volume.png" onclick="buttonAction('increase')" style="cursor:pointer; width=100px;" alt="Image 6"/>
    <img src="/static/lower_volume.png" onclick="buttonAction('decrease')" style="cursor:pointer; width=100px;" alt="Image 7"/>

    <p id="result"></p>
</body>
</html>
"""

# Serve the HTML page
@app.route('/')
async def index(request):
    return html(HTML_CONTENT)

# define the different train objects
train_music    = Train("music")
train_horn     = Train("horn")
train_wheels   = Train("wheels")
train_engine   = Train("engine")
old_music_state = "stop"

# define a Serial object to communicate with Arduino
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
ser.reset_input_buffer()

async def control_engine_LEDs():
    if global_dict["leds"]["state"]:
        # LEDs are on, so turn them off
        ser.write(b"Turn LEDs off\n")
    else:
        ser.write(b"Turn LEDs on\n")

async def control_smoke():
    if global_dict["smoke"]["state"]:
        # smoke is running, so turn it off
        ser.write(b"Turn smoke off\n")
    else:
        ser.write(b"Turn smoke on\n")

async def control_lights():
    if global_dict["lights"]["state"]:
        # if state = True/on, then turn them off
        ser.write(b"Turn lights off\n")
    else:
        # state = False/off, so turn on lights
        ser.write(b"Turn lights on\n")

async def control_horn():
    # play from the RPi
    #train_horn.next_song()
    print(f"Playing horn sound now")

async def control_wheels():
    if global_dict["wheels"]["state"]:
        # wheels are spinning already, so turn them off
        ser.write(b"Stop wheels\n")
    else:
        ser.write(b"Start wheels\n")

async def pps_song(new_music_state):
    # play, pause, or stop song
    global old_music_state

    if new_music_state == "play":
        if old_music_state == "stop":
            #train_music.play_song()
            print(f"Hit play from stop")
        elif old_music_state == "pause":
            #train_music.resume_song()
            print(f"Hit play from pause")
    elif new_music_state == "pause":
        if old_music_state == "play":
            #train_music.pause_song()
            print(f"Hit pause from play")
    elif new_music_state == "stop":
        if old_music_state != "stop":
            #train_music.stop_song()
            print(f"Hit stop from play or pause")
    old_music_state = new_music_state

    msg = f"Song status is {new_music_state}"
    return {"message":msg}


async def change_song(state):
    global old_music_state

    if state == "next":
        #train_music.next_song()
        print(f"Went to next song")
    elif state == "previous":
        #train_music.previous_song()
        print(f"Went to previous song")

    msg = f"Moved to {state} song"
    old_music_state = "play"
    return {"message":msg}

async def set_volume(state):
    global old_music_state

    if old_music_state == "play":
        #vol = train_music.get_volume()
        if state == "increase":
            #vol += 10
            print(f"Increased volume")
        elif state == "decrease":
            #vol -= 10
            print(f"Decreased volume")
        #train_music.set_volume(vol)

        msg = f"{state}d volume"
    else:
        msg = f"Not changing volume; nothing playing"
    return {"message":msg}


global_dict    = {"smoke":{"state":False,"function":control_smoke},
                  "lights":{"state":False,"function":control_lights},
                  "horn":{"state":False,"function":control_horn},
                  "wheels":{"state":False,"function":control_wheels},
                  "leds":{"state":False,"function":control_engine_LEDs}
                 }

# Asynchronous actions triggered by buttons

music_control_list = ["play", "previous", "next", "pause", "stop", "increase", "decrease"]

@app.route('/action/<action>')
async def perform_action(request, action):
    if action == "play" or action == "pause" or action == "stop":
        result = await pps_song(action)
    elif action == "next" or action == "previous":
        result = await change_song(action)
    elif action == "increase" or action == "decrease":
        result = await set_volume(action)
    else:
        # it's the state toggling
        result = await toggle_states(action)

    return json(result)

async def toggle_states(action):
    global global_dict

    await asyncio.sleep(1)

    global_dict[action]["state"] = not global_dict[action]["state"]
    msg = f"Turned {action} to {global_dict[action]['state']}"
    return {"message":msg}

# Run the app
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000)
    except KeyboardInterrupt:
        print(f"Peace out yo!")

