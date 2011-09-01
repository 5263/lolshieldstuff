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

// Initialize char array for text string
byte text[MAX_TEXT_LENGTH];
uint8_t ringbufferread=0;
uint8_t ringbufferwrite=0;

void setup() {
  Serial.begin(9600);
  LedSign::Init();
  
  text[0] = 'Test';
  //getLength(text, &textLength, &totalPixels);
}


int readytowrite()
{
  bool rtw=(Serial.available()>0 && (ringbufferread)!=((ringbufferwrite+1) & (MAX_TEXT_LENGTH-1)));
  return rtw;
}

void getNewText() {
 while (readytowrite())
  {
    text[ringbufferwrite] = byte(Serial.read());
    ringbufferwrite = (ringbufferwrite+1) & (MAX_TEXT_LENGTH-1);
  }
  if ((ringbufferread)!=((ringbufferwrite+1) & (MAX_TEXT_LENGTH-1)))
  {
    uint8_t freebytes=(int(ringbufferread)-int(ringbufferwrite)-1) & 
      (MAX_TEXT_LENGTH-1);
    if (freebytes < 10)
      Serial.write(freebytes+0x30);
    else
    {
      Serial.write(((freebytes >> 4) + 0x41));   //notify client with number of free bytes in buffer
     }
  }
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
  if (ringbufferread != ringbufferwrite)
  {
      byte nextchar=text[ringbufferread];
      ringbufferread = (ringbufferread+1) & (MAX_TEXT_LENGTH-1);
      if (nextchar ==' ') for (int i=0; i<4; i++)
      {
	LedSign::ScrollLeft(1,0);
	//for (int wc=0; wc<6;wc++)
	//{
	  getNewText();
	  delay(SCROLL_DELAY);  
	//}
      }
      else
      {
	 byte charlength = Font::CharLength(nextchar);
         for (uint8_t x=0; x<charlength; x++)
	 {
           LedSign::ScrollLeft(1,0);
           Font::DrawLine(nextchar,X_MAX,0,x,1);
   	   //for (int wc=0; wc<6;wc++)
	   //{
	     getNewText();
	     delay(SCROLL_DELAY);  
	    //}
	 }
         //Serial.write('S');
	 //LedSign::ScrollLeft(1,0);
	 //delay(SCROLL_DELAY);
      }
  }
  getNewText();
}  
 
  


