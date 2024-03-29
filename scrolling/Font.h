/*
  Font drawing library

  Copyright 2009/2010 Benjamin Sonntag <benjamin@sonntag.fr> http://benjamin.sonntag.fr/
  
  History:
  	2010-01-01 - V0.0 Initial code at Berlin after 26C3
  	2011-08-23 - lamer had to mofify the integer types to make
  			the header compatible to ikkei's Font.cpp


  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place - Suite 330,
  Boston, MA 02111-1307, USA.
*/

#ifndef Font_h
#define Font_h

#include <inttypes.h>

namespace Font
{
extern uint8_t Draw(uint16_t letter,uint8_t x,uint8_t y,uint8_t set=1);
/*extern uint8_t Draw(unsigned char letter,int x,int y,int set=1); */
extern uint8_t Draw90(uint16_t letter,uint8_t x,uint8_t y,uint8_t set=1);
/*extern uint8_t Draw90(unsigned char letter,int x,int y,int set=1); */
extern uint8_t CharLength(uint16_t letter);
extern uint8_t DrawLine(uint16_t letter,uint8_t x,uint8_t y,uint8_t i,
        uint8_t set);

}

#endif

