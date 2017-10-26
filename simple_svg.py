#!/usr/bin/env python
"""
This is a software-only implementation to create svg files using the same
algorithm as the Arduino code. Allows me to play around with the range of
settings with quick turnaround before programming the Arduino.


SVG.py - Construct/display SVG scenes.

The following code is a lightweight wrapper around SVG files. The metaphor
is to construct a scene, add objects to it, and then write it to a file
to display it.

This program uses ImageMagick to display the SVG files. ImageMagick also 
does a remarkable job of converting SVG files into other formats.
"""

import os
import random
import math
display_prog = 'display' # Command to execute to display images.
      
class Scene:
    def __init__(self,name="svg",height=400,width=400):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        return

    def add(self,item): self.items.append(item)

    def strarray(self):
        var = ["<?xml version=\"1.0\"?>\n",
               "<svg height=\"%d\" width=\"%d\" >\n" % (self.height,self.width),
               " <g style=\"fill-opacity:1.0; stroke:black;\n",
               "  stroke-width:1;\">\n"]
        for item in self.items: var += item.strarray()            
        var += [" </g>\n</svg>\n"]
        return var

    def write_svg(self,filename=None):
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open(self.svgname,'w')
        file.writelines(self.strarray())
        file.close()
        return

    def display(self,prog=display_prog):
        os.system("%s %s" % (prog,self.svgname))
        return        
        

class Line:
    def __init__(self,start,end):
        self.start = start #xy tuple
        self.end = end     #xy tuple
        return

    def strarray(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" />\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1])]


class Circle:
    def __init__(self,center,radius,color):
        self.center = center #xy tuple
        self.radius = radius #xy tuple
        self.color = color   #rgb tuple in range(0,256)
        return

    def strarray(self):
        return ["  <circle cx=\"%d\" cy=\"%d\" r=\"%d\"\n" %\
                (self.center[0],self.center[1],self.radius),
                "    style=\"fill:%s;\"  />\n" % colorstr(self.color)]

class Rectangle:
    def __init__(self,origin,height,width,color):
        self.origin = origin
        self.height = height
        self.width = width
        self.color = color
        return

    def strarray(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %\
                (self.origin[0],self.origin[1],self.height),
                "    width=\"%d\" style=\"fill:%s;\" />\n" %\
                (self.width,colorstr(self.color))]

class Text:
    def __init__(self,origin,text,size=24):
        self.origin = origin
        self.text = text
        self.size = size
        return

    def strarray(self):
        return ["  <text x=\"%d\" y=\"%d\" font-size=\"%d\">\n" %\
                (self.origin[0],self.origin[1],self.size),
                "   %s\n" % self.text,
                "  </text>\n"]
        
    
def colorstr(rgb): return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)

def test():
    scene = Scene('test', 1024, 1024)
    pos = 0
    spd = 0.005
    decay = 60000

    random.seed()
    facter = 1.001 + random.random() * 0.02
    starter = 3.141 * random.random()
    facter2 = 0.99 + random.random() * 0.02
    starter2 = 3.141 * random.random()
    decay = 100000 + int(random.random() * 100000)
    prevx = 512
    prevy = 512
    for pos in range(decay/20, decay):
        adjx = int(512 + int(256 * (pos/float(decay)) * math.sin(pos * spd)))
        adjy = int(512 + int(256 * (pos/float(decay)) * math.cos(starter + (pos * spd * facter))))
        adjx += int(256 * (pos/float(decay)) * math.sin(starter2 + (pos * spd*facter2)))
        adjy += int(256 * (pos/float(decay)) * math.cos(starter2 + (pos * spd*facter2)))
        scene.add(Line((prevx,prevy),(adjx, adjy)))
        prevx = adjx
        prevy = adjy

    scene.write_svg()
    scene.display()
    return

if __name__ == '__main__': test()

