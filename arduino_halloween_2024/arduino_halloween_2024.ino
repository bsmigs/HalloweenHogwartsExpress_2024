#include <Adafruit_NeoPixel.h>

// Number of WS2812B LEDs attached to the Arduino
#define MAX_LED_COUNT 300
#define LED_COUNT 40
#define LED_PIN 6
#define LIGHTS_PIN 7
#define SMOKE_PIN 8
#define WHEELS_PIN 9
#define FRONT_ENABLE_PIN_A 2
#define FRONT_ENABLE_PIN_B 3
#define L298N_1_IN1_PIN 5
#define L298N_1_IN2_PIN 6
#define L298N_1_IN3_PIN 7
#define L298N_1_IN4_PIN 8
#define BAUD_RATE 9600

enum motor_state 
{
  START,
  STOP
};

// Setting up the NeoPixel library
Adafruit_NeoPixel strip(MAX_LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void motor_controller_setup()
{
  // for the first motor controller (front two motors)
  pinMode(FRONT_ENABLE_PIN_A, OUTPUT);
  pinMode(FRONT_ENABLE_PIN_B, OUTPUT);
  pinMode(L298N_1_IN1_PIN, OUTPUT);
  pinMode(L298N_1_IN2_PIN, OUTPUT);
  pinMode(L298N_1_IN3_PIN, OUTPUT);
  pinMode(L298N_1_IN4_PIN, OUTPUT);

  // Turn off motors - Initial state
  digitalWrite(L298N_1_IN1_PIN, LOW);
  digitalWrite(L298N_1_IN2_PIN, LOW);
  digitalWrite(L298N_1_IN3_PIN, LOW);
  digitalWrite(L298N_1_IN4_PIN, LOW);
}

void motor_function(enum motor_state function)
{
  analogWrite(FRONT_ENABLE_PIN_A, 255);
  analogWrite(FRONT_ENABLE_PIN_B, 255);
  
  switch (function)
  {
    case START: // forward
      digitalWrite(L298N_1_IN1_PIN, HIGH);
      digitalWrite(L298N_1_IN2_PIN, LOW);
      digitalWrite(L298N_1_IN3_PIN, HIGH);
      digitalWrite(L298N_1_IN4_PIN, LOW);
      break;
    case STOP: // stop
      digitalWrite(L298N_1_IN1_PIN, LOW);
      digitalWrite(L298N_1_IN2_PIN, LOW);
      digitalWrite(L298N_1_IN3_PIN, LOW);
      digitalWrite(L298N_1_IN4_PIN, LOW);
      break;
    default: // stop
      digitalWrite(L298N_1_IN1_PIN, LOW);
      digitalWrite(L298N_1_IN2_PIN, LOW);
      digitalWrite(L298N_1_IN3_PIN, LOW);
      digitalWrite(L298N_1_IN4_PIN, LOW);
      break;
  }
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  pinMode(LIGHTS_PIN, OUTPUT);
  digitalWrite(LIGHTS_PIN, LOW);

  pinMode(SMOKE_PIN, OUTPUT);
  digitalWrite(SMOKE_PIN, LOW);

  pinMode(WHEELS_PIN, OUTPUT);
  digitalWrite(WHEELS_PIN, LOW);

  // setup L298N H-bridge motor controller pins
  motor_controller_setup();
  
  // initialization for the LED strip around engine
  strip.begin();           // Initialize NeoPixel object
  strip.setBrightness(10); // Set BRIGHTNESS to about 4% (max = 255)
  strip.show();            // Initialize all pixels to 'off'

  // if I am going to change the number of LEDs being used
  // make sure I update that here after everything is cleared out
  strip.updateLength(LED_COUNT);
  delay(100);
}

void loop() {
  if (Serial.available() > 0)
  {
    String data_from_rpi = Serial.readStringUntil('\n');
    Serial.print("RPi sent me: ");
    Serial.println(data_from_rpi);

    if (data_from_rpi == "Turn lights on")
    {
      digitalWrite(LIGHTS_PIN, HIGH);
    }
    else if (data_from_rpi == "Turn lights off")
    {
      digitalWrite(LIGHTS_PIN, LOW);
    }
    else if (data_from_rpi == "Turn LEDs on")
    {
      rainbow(10);
    }
    else if (data_from_rpi == "Turn LEDs off")
    {
      strip.show();
    }
    else if (data_from_rpi == "Turn smoke on")
    {
      digitalWrite(SMOKE_PIN, HIGH);
    }
    else if (data_from_rpi == "Turn smoke off")
    {
      digitalWrite(SMOKE_PIN, LOW);
    }
    else if (data_from_rpi == "Start wheels")
    {
      motor_function(START);
    }
    else if (data_from_rpi == "Stop wheels")
    {
      motor_function(STOP);
    }
    
    
  }
  //rainbow(10);
  //snowflakes(100)

  /*
  // Do a theater marquee effect in various colors...
  theaterChase(strip.Color(255, 255, 255), 50); // White
  theaterChase(strip.Color(255,   0,   0), 50); // Red
  theaterChase(strip.Color(  0,   0, 255), 50); // Blue
   */
}

// Rainbow cycle along whole strip. Pass delay time (in ms) between frames.
void rainbow(int wait) {
  // 5 cycles of all colors on wheel
  for(long firstPixelHue = 0; firstPixelHue < 5*65536; firstPixelHue += 256) {
    strip.rainbow(firstPixelHue);
    strip.show(); // Update strip with new contents
    delay(wait);  // Pause for a moment
  }
}

void snowflakes(uint8_t wait) {
  // Setup the pixel array
  int pixel[60];
  for(int p=0; p<60; p++){
    pixel[p] = random(0,255); 
  }
  
  // Run some snowflake cycles
  for (int j=0; j<200; j++) {
    // Every five cycles, light a new pixel
    if((j%5)==0){
      strip.setPixelColor(random(0,60), 255,255,255);
    }
    
    // Dim all pixels by 10
    for(int p=0; p<60; p++){
      strip.setPixelColor(p, pixel[p],pixel[p],pixel[p] );
      pixel[p] =  pixel[p] - 10;
    }
    strip.show();
    delay(wait);
  }
}

// Theater-marquee-style chasing lights. Pass in a color, and 
// a delay time (in ms) between frames.
void theaterChase(uint32_t color, int wait) {
  for(int a=0; a<10; a++) {  // Repeat 10 times...
    for(int b=0; b<3; b++) { //  'b' counts from 0 to 2...
      strip.clear();         //   Set all pixels in RAM to 0 (off)
      // 'c' counts up from 'b' to end of strip in steps of 3...
      for(int c=b; c<strip.numPixels(); c += 3) {
        strip.setPixelColor(c, color); // Set pixel 'c' to value 'color'
      }
      strip.show(); // Update strip with new contents
      delay(wait);  // Pause for a moment
    }
  }
}
