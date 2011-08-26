#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cPickle

def fontshitcharstoright(charlst):
    '''shifts characters to the left to allow the display lib
    to remove whitespace on the right
    warning: modifies the charaters in place'''
    for singlecharlst in charlst:
        for dontcare in xrange(5):
            if singlecharlst[0]==0:
                del singlecharlst[0]
                singlecharlst.append(0)
            else:
                break

def createfontfromimage():
    import Image
    img=Image.open('a02-cut.pbm')
    debugimg=img.copy().convert('RGB')
    charlst=[]
    for charnum in xrange(256):
        xcell=int(1502/15.0*(charnum >> 4))
        ycell=int(1916/15.0*(charnum & 15))
    #    print charnum,xcell,ycell
        singlecharlst=[]
        for x in range(5):
            xcoord=xcell+18+int((x+0.5)*(79+1-18)/(5.0))
            bitfield=0
            for y in xrange(8):
                ycoord=ycell+int((y+0.5)*(100/8.0))
                value=(img.getpixel((xcoord,ycoord)) & 1) ^ 1
                debugimg.putpixel((xcoord,ycoord),(255,0,0))
                bitfield += value << y
            singlecharlst.append(bitfield)
        charlst.append(singlecharlst)
    debugimg.save('debug.png')
#    pf=open('a02.pickle','wb')
#    cPickle.dump(charlst,pf)
#    pf.close()

def createfont(charlst1,charlst2,charlst1min,charlst2min):
    def encodechars(charlst):
        #'{ 0x00, 0x00, 0x00, 0x00, 0x00 },'
        return ',\n'.join([ '{ %s }' % ', '.join([hex(bitfield) \
                for bitfield in singlecharlst]) for singlecharlst in charlst])

    charlst1max=charlst1min+len(charlst1)-1
    charlst2max=charlst2min+len(charlst2)-1
    formatoptions={'dotfont1': encodechars(charlst1),
            'dotfont2' : encodechars(charlst2),
            'fontMin1hex' : hex(charlst1min),
            'fontMax1hex' : hex(charlst1max),
            'fontMin2hex' : hex(charlst2min),
            'fontMax2hex' : hex(charlst2max)}

    fontcppformat='''/*
  Font drawing library

  Copyright 2009/2010 Benjamin Sonntag <benjamin@sonntag.fr> http://benjamin.sonntag.fr/
  
  History:
  	2010-01-01 - V0.0 Initial code at Berlin after 26C3
  	2010-09-10 - ikkei replaced font data to bit map font
  				 that is similar LCD SC-1602BS Standard Character Pattern
  				 and place to flash memory
  				<ikkei@zeus.eonet.ne.jp> http://blog.goo.ne.jp/jh3kxm
  	2011-08-23 - lamer replaced font data using a custom python skript

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



#include "Font.h"
#include "Charliplexing.h"
#include <inttypes.h>
#include <avr/pgmspace.h>

uint8_t dotfont1[][5] PROGMEM = {
%(dotfont1)s
};

uint8_t dotfont2[][5] PROGMEM = {
%(dotfont2)s
};

uint16_t fontMin1=%(fontMin1hex)s;
uint16_t fontMax1=%(fontMax1hex)s;
uint16_t fontMin2=%(fontMin2hex)s;
uint16_t fontMax2=%(fontMax2hex)s;


/* -----------------------------------------------------------------  */
/** Draws a figure (0-9). You should call it with set=1, 
 * wait a little them call it again with set=0
 * @param figure is the figure [0-9]
 * @param x,y coordinates, 
 * @param set is 1 or 0 to draw or clear it
 */
 
uint8_t Font::Draw(uint16_t letter,int x,int y,int set) {
  uint16_t maxx = 0;
  uint16_t font_data = 0;
  int i,j;
  
  if ( letter==' ' ) return 3+2;
  if ( letter<fontMin1 || letter>fontMax2 ) return 0;
  if ( letter>fontMax1 && letter<fontMin2 ) return 0;

  for ( i=0; i<5; i++){
   	if ( letter <= fontMax1 ){
   	  font_data = pgm_read_byte( &(dotfont1[ letter - fontMin1 ][i]));
   	}else{
   	  font_data = pgm_read_byte( &(dotfont2[ letter - fontMin2 ][i]));
   	}
   	if ( font_data != 0 ){
	  if ( i > maxx ){
	    maxx = i;
	  }
	}
	if ( (i+x)<14 && (i+x)>=0 ){
	  for ( j=0; j<8; j++ ){
		if ( (j+y)<9 && (j+y)>=0 ){
		  if ( font_data & (1<<j)){
		    LedSign::Set(i+x, j+y, set);
		  }
		}
	  }
	}
  }
  return (maxx+2);
}



/* -----------------------------------------------------------------  */
/** Draw a figure in the other direction (rotated 90deg)
 * You should call it with set=1, 
 * wait a little them call it again with set=0
 * @param figure is the figure [0-9]
 * @param x,y coordinates, 
 * @param set is 1 or 0 to draw or clear it
*/

uint8_t Font::Draw90(uint16_t letter,int x,int y,int set) {
  uint16_t maxx = 0;
  uint16_t font_data = 0;
  int i,j;
  
  if ( letter==' ' ) return 3+2;
  if ( letter<fontMin1 || letter>fontMax2 ) return 0;
  if ( letter>fontMax1 && letter<fontMin2 ) return 0;

  for ( i=0; i<5; i++){
   	if (letter <= fontMax1){
   	  font_data = pgm_read_byte( &(dotfont1[ letter - fontMin1 ][i]));
   	}else{
   	  font_data = pgm_read_byte( &(dotfont2[ letter - fontMin2 ][i]));
   	}
	if ( (6-i+y)<9 && (6-i+y)>=0 ){
	  for ( j=0; j<8; j++ ){
	  	if ( font_data & (1<<j)){
		  if ( j > maxx ){
		    maxx = j;
		  }
		  if ( (j+x+1)<14 && (j+x+1)>=0 ){
		    LedSign::Set(j+x+1, 6-i+y, set);
		  }
		}
	  }
	}
  }
  return (maxx+2);
}
'''
    return fontcppformat % formatoptions

def writefontfile(charlst):
    outfile=open('Font-a02.cpp','w')
    outfile.write(createfont(charlst[0:16],charlst[16:256],0,16))
    outfile.close()

charlst=cPickle.load(file('a02.pickle','rb'))
#fontshitcharstoright(charlst)
#def writefontfile(charlst):

#fontshitcharstoright(charlst)
#printstring(raw_input())

#print createfont(charlst[0:16],charlst[16:256],0,16)
#print len(charlst[0:16]),len(charlst[16:256])
#print len(charlst)
