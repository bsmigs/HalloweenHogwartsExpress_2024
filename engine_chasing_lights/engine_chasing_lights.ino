#include <Adafruit_NeoPixel.h>

// Pin to use to send signals to WS2812B
#define LED_PIN 6

// Number of WS2812B LEDs attached to the Arduino
#define MAX_LED_COUNT 100
#define LED_COUNT 50

// Setting up the NeoPixel library
Adafruit_NeoPixel strip(MAX_LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();           // Initialize NeoPixel object
  strip.setBrightness(10); // Set BRIGHTNESS to about 4% (max = 255)
  strip.show();            // Initialize all pixels to 'off'

  // if I am going to change the number of LEDs being used
  // make sure I update that here after everything is cleared out
  strip.updateLength(LED_COUNT);
  delay(100);
}

void loop() {
  // Do a theater marquee effect in various colors...
  theaterChase(strip.Color(255, 255, 255), 50); // White
  theaterChase(strip.Color(255,   0,   0), 50); // Red
  theaterChase(strip.Color(  0,   0, 255), 50); // Blue
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
