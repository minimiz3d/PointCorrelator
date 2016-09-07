#!/usr/bin/env python

import sys, os
import pygame
from pygame.locals import *

# Constants
BACKGROUND_COLOR = (250,250,250)
WIDTH, HEIGHT = 1024, 768
# (...)

class PointCorrelator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
        self.picture = pygame.image.load("didi.jpg")

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.screen.blit(pygame.transform.scale(self.picture,(WIDTH, HEIGHT)),(0,0))

        pygame.display.flip()

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


# Exception Handling
if __name__ == '__main__':
    # (...)

    pt_corr = PointCorrelator()
    pt_corr.mainLoop()
