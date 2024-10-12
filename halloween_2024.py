from sanic import Sanic
from sanic.response import html, json
import asyncio
from train import Train

app = Sanic("ButtonApp")

# HTML content with buttons that make asynchronous requests
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hogwarts Page</title>
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
    <button onclick="buttonAction('smoke')">Release Smoke</button>
    <button onclick="buttonAction('lights')">Turn Lights On/Off</button>
    <button onclick="buttonAction('horn')">Play Train Horn</button>
    <button onclick="buttonAction('wheels')">Turn Wheels On/Off</button>
    
    <h2>Music Controls</h2>
    <button onclick="buttonAction('play')">Play Song</button>
    <button onclick="buttonAction('pause')">Pause Song</button>
    <button onclick="buttonAction('stop')">Stop Song</button>
    <button onclick="buttonAction('next')">Next Song</button>
    <button onclick="buttonAction('previous')">Previous Song</button>
    <button onclick="buttonAction('increase')">Increase Volume</button>
    <button onclick="buttonAction('decrease')">Decrease Volume</button>

    <p id="result">Result will appear here</p>
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

async def control_smoke():
    return 0

async def control_lights():
    return 0

async def control_horn():
    return 0

async def control_wheels():
    return 0

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
                  "wheels":{"state":False,"function":control_wheels}
                 }
'''
music_state    = "stop"
music_dict     = {"play":{"state":"resume","function":pps_song},
                  "pause":{"state":"pause","function":pps_song},
                  "stop":{"state":"stop","function":pps_song},
                  "next":{"state":"resume","function":change_song},
                  "previous":{"state":"resume","function":change_song},
                  "increase":{"state":"resume","function":set_volume},
                  "decrease":{"state":"resume","function":set_volume}
                 }
'''

# Asynchronous actions triggered by buttons
'''
@app.route('/action/<action>')
async def perform_action(request, action):
    result = await toggle_states(action)
    return json(result)
'''

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

