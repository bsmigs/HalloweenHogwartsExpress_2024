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
  snowflakes(100);
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
