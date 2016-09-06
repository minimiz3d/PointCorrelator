#!/usr/bin/env python

import sys, os
import pygame
from pygame.locals import *
from random import randint
from utils import *

WIDTH, HEIGHT = 1024, 768
BACKGROUND_COLOR = (200,200,200)
LINE_COLOR = (0,0,0)
POINT_COLOR = (0,150,0)
LINE_WIDTH = 2
POINT_RADIUS = 6
POINTS_TO_ADD = 100
MIN_DIST = 15

class ShowMapAndPoints(object):
    def __init__(self, lines_filename, points_filename):
        pygame.init()
        self.lines_filename = lines_filename
        self.points_filename = points_filename
        self.screen = \
                pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
        self.lines = list()
        self.points = list()
        self.load_lines()
        self.load_points()
    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for line in self.lines:
            start, end = line
            pygame.draw.line(self.screen, LINE_COLOR, \
                    start, end, LINE_WIDTH)
        for point in self.points:
            pygame.draw.circle(self.screen, POINT_COLOR, \
                    point, POINT_RADIUS)
        pygame.display.flip()
    def load_points(self):
        if not os.path.exists(self.points_filename):
            return
        f = open(self.points_filename, 'r')
        for string in f.readlines():
            x,y = [int(x) for x in string.split(',')]
            self.points.append((x,y))
        f.close()
    def load_lines(self):
        if not os.path.exists(self.lines_filename):
            return
        f = open(self.lines_filename, 'r')
        for string in f.readlines():
            x0,y0,x1,y1 = \
                    [int(x) for x in string.split(',')]
            p0 = (x0, y0)
            p1 = (x1, y1)
            self.lines.append((p0,p1))
        f.close()
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return False

        return True
    def mainLoop(self):
        while self.events():
            self.draw()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ("Usage: %s filename.map filename.pts") % sys.argv[0]
    smp = ShowMapAndPoints(sys.argv[1], sys.argv[2])
    smp.mainLoop()
