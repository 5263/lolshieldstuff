/*
  Requires LoL Shield library, at least V0.2Beta 
  http://code.google.com/p/lolshield/downloads/list

  Based on original TEXT SAMPLE CODE for LOL Shield for Arduino
  Copyright 2009/2010 Benjamin Sonntag <benjamin@sonntag.fr> http://benjamin.sonntag.fr/
  
  (Serial version edited by Walfas)
  minor changes applied by lamer
*/

#include "Charliplexing.h"
#include "Font.h"
#include "WProgram.h"

// The number of columns of LEDs minus one
#define X_MAX 13

// Scroll delay: lower values result in faster scrolling
#define SCROLL_DELAY 60

/* How long to wait after the last letter before
    going to the next message or starting over again */
#define NEXT_MSG_DELAY 0

#define MAX_TEXT_LENGTH 256 // Max number of characters in string

/* Print these values when trying to get the next part of the 
    current message or a new message. */
#define GET_MORE 'g'
#define GET_NEW 'n'

/* Used to calculate how many characters are in a string 
    and how many pixels that string takes up horizontally. */
int textLength, totalPixels;

// Initialize char array for text string
byte text[MAX_TEXT_LENGTH];

void getLength(byte* charArray, int* lengthPtr, int* pixelPtr) ;
void getNewText(unsigned char* charArray) ;
void setup() {
  Serial.begin(9600);
  LedSign::Init();
  
  text[0] = '\0';
  getLength(text, &textLength, &totalPixels);
}

void testcharset() {
  for(int x=0x0; x<=255; x++) {
    LedSign::Clear();
    Font::Draw(x,0,0,1);
    //Font::Draw(((x/10)%10)+3*16,5,0,1);
    //Font::Draw((x%10)+3*16,10,0,1);
    //LedSign::Set(0,5,1);
    LedSign::Set(6,0,((x>>7)&1));
    LedSign::Set(7,0,((x>>6)&1));
    LedSign::Set(8,0,((x>>5)&1));
    LedSign::Set(9,0,((x>>4)&1));
    LedSign::Set(10,0,((x>>3)&1));
    LedSign::Set(11,0,((x>>2)&1));
    LedSign::Set(12,0,((x>>1)&1));
    LedSign::Set(13,0,(x&1));
    delay(100);
  }
}

void loop() {
  // Read text from serial and determine the length
  LedSign::Clear();
  getNewText(text);
  getLength(text, &textLength, &totalPixels);
  
  // Output the characters to the LED matrix
  int x=0;
  for(int j=X_MAX; j>-totalPixels-X_MAX; j--) {
    x=j;
    LedSign::Clear();
    
    // Draw each character, offset by x "pixels"
    for(int i=0; i<textLength; i++) {
      x += Font::Draw(text[i],x,0,1);
      
      // If the character is off the screen, stop.
      if (x>=X_MAX) 
        break;
    }
    // Wait before moving everything to the left by one
    delay(SCROLL_DELAY);
  }
  // Wait before displaying the next message
  delay(NEXT_MSG_DELAY);
}

void getNewText(unsigned char* charArray) {
  /* Gets a new string from the serial port. */
  byte charRead = '0';
  int charCount = 0;
  boolean waiting = false;
  
  // Request a new string
  Serial.write(GET_NEW);
  
  /* If the string is sent in multiple 
      parts, get each one separately */
  while (charCount < MAX_TEXT_LENGTH && charRead != '\n' && charRead != '\0') {
    if (!waiting) {
      Serial.write(GET_MORE); // Request next part of string
      waiting = true;
    }
    
    while (Serial.available()) {
      charRead = byte(Serial.read());
      charArray[charCount] = charRead;
      charCount++;
      waiting = false;
    }
  }
  
  // Append a null character to the end
  charArray[charCount] = '\0';
}

void getLength(byte* charArray, int* lengthPtr, int* pixelPtr) {
  /* Finds the length of a string in terms of characters
     and pixels and assigns them to the variable at 
     addresses lengthPtr and pixelPtr, respectively. */
      
  int charCount = 0, pixelCount = 0;
  byte * charPtr = charArray;
  
  // Count chars until newline or null character reached
  while (charArray[charCount] != '\0' && charArray[charCount] != '\n') {
    charPtr++;
    charCount++;
    
    /* Increment pixelCount by the number of pixels 
       the current character takes up horizontally. */
    pixelCount += Font::Draw(charArray[charCount],-X_MAX,0);
  }

  *pixelPtr = pixelCount;
  *lengthPtr = charCount;
}
