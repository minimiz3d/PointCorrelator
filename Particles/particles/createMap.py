#!/usr/bin/env python

import sys, os
import pygame
from pygame.locals import *

WIDTH, HEIGHT = 1024, 768
BACKGROUND_COLOR = (200,200,200)
LINE_COLOR = (0,0,0)
WORKLINE_COLOR = (255,0,0)
LINE_WIDTH = 5

class CreateMap(object):
    def __init__(self, filename):
        pygame.init()
        self.filename = filename
        self.screen = \
                pygame.display.set_mode((WIDTH, HEIGHT))
        self.lines = list()
        self.lastPoint = None
        self.workingLine = None
        self.load()
    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for line in self.lines:
            start, end = line
            pygame.draw.line(self.screen, LINE_COLOR, \
                    start, end, LINE_WIDTH)
        if self.workingLine is not None:
            start, end = self.workingLine
            pygame.draw.line(self.screen, WORKLINE_COLOR,\
                    start, end, LINE_WIDTH)
        pygame.display.flip()
    def load(self):
        if not os.path.exists(self.filename):
            return
        f = open(self.filename, 'r')
        for string in f.readlines():
            x0,y0,x1,y1 = \
                    [float(x) for x in string.split(',')]
            p0 = (x0, y0)
            p1 = (x1, y1)
            self.lines.append((p0,p1))
        f.close()
    def save(self):
        f = open(self.filename, 'w')
        for line in self.lines:
            p0, p1 = line
            x0, y0 = p0
            x1, y1 = p1
            f.write('%d,%d,%d,%d\n' % (x0, y0, x1, y1))
        f.close()
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.save()
                    return False
                elif event.key == pygame.K_ESCAPE:
                    self.lastPoint = None
                    self.workingLine = None
                elif event.key == pygame.K_BACKSPACE:
                    self.lines = list()
            elif event.type == pygame.MOUSEMOTION:
                start = self.lastPoint
                end = event.pos
                if start is not None:
                    self.workingLine = (start, end)
            elif event.type == pygame.MOUSEBUTTONUP:
                start = self.lastPoint
                end = event.pos
                self.lastPoint = end
                if start is not None:
                    self.lines.append((start, end))
        return True
    def mainLoop(self):
        while self.events():
            self.draw()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("Usage: %s filename.map") % sys.argv[0]
    cm = CreateMap(sys.argv[1])
    cm.mainLoop()
