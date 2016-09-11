#!/usr/bin/env python

import sys, os
import pygame
import operator
from operator import itemgetter
from pygame.locals import *

# Constants
BACKGROUND_COLOR = (250,250,250)
BLACK = (0,0,0)
WIDTH, HEIGHT = 640, 480
POINT_COLOR = (0, 150, 0)
HIGHLIGHT_COLOR = (150, 0, 0)
POINT_RADIUS = 3
HIGHLIGHT_RADIUS = 5
HIGHLIGHT_WIDTH = 2
CLICK_PRECISION = 5

class PointCorrelator(object):
    def __init__(self, pointsFile, imageFile, filename):
        pygame.init()               # initializes pygame modules
        self.pointsFile = pointsFile
        self.imageFile = imageFile
        self.filename = filename

        self.points_list = list()
        self.highlighted_points = list()                                    # stores highlighted points
        self.connectedPoints = list()                                       # stores connected points

        self.connectionExists = 0
        self.lastHighlight = 0
        self.finishingPoint = 0
        self.point_to_highlight = 0
        self.firstclick = 0

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)   # set screen mode
        self.loadPoints()                                                   # loads file with point data
        self.loadImage()                                                    # loads image that the points will be connected to

    def loadPoints(self):
        pts = open(self.pointsFile, 'r')                    # opens file with points read-only
        for string in pts.readlines():                      # reads file line by line, getting x and y information
            x, y = [int(x) for x in string.split(',')]      # evil string manipulation
            self.points_list.append((x,y))                  # appends new points to points list
        pts.close()                                         # close file (good programming!)

        self.ptsSurface = pygame.Surface((max(self.points_list, key=itemgetter(0))[0], \
                        max(self.points_list, key=itemgetter(1))[1]))   # creates surface for drawing the points
                                                                        # of the size max(x), max(y)

        self.highlightSurface = pygame.Surface(self.screen.get_size())          # creates new surface with same size as ptsSurface
        # this will be used for highlighting points
        self.highlightSurface.set_colorkey((0, 0, 0))                               # set transparency color to black
        #       self.ptsSurface = pygame.transform.scale(self.ptsSurface, (300, 300))       # resize the surface (only resizes the actual

    def loadImage(self):
        self.imgSurface = pygame.image.load(self.imageFile)

    def resize(self, new_width, new_height):
        self.screen = pygame.display.set_mode((new_width, new_height), RESIZABLE)   # set new mode for the screen when the window
                                                                                    # is resized
        self.highlightSurface = pygame.transform.scale(self.highlightSurface, (new_width, new_height))

    # This method tests if a point clicked on the screen is in the points_list
    # loaded from the file. This ensures that only points present in the list
    # can be selected
    def checkPoint(self, point_clicked):
        print point_clicked
        is_in = False
        for point in self.points_list:
            if point_clicked[0] < point[0] + CLICK_PRECISION and point_clicked[1] < point[1]\
            + CLICK_PRECISION and point_clicked[0] > point[0] - CLICK_PRECISION \
            and point_clicked[1] > point[1] - CLICK_PRECISION:                      # yeah, this is pretty fucking ugly
                is_in = True
                break
        if is_in is True: return point        # returns point where the click happened
        else: return None

    def addCircle(self):
        already_highlighted = 0

        for tup in self.highlighted_points:
            if self.point_to_highlight == tup:
                already_highlighted = 1
                break

        if(already_highlighted == 0):
            print "Highlighting %s" % (self.point_to_highlight, )
            self.lastHighlight = self.point_to_highlight                              # saves last highlighted point
            self.finishingPoint = self.lastHighlight
            self.highlighted_points.append(self.point_to_highlight)
            self.connectionExists = 0
    def addLine(self):
        print "Drawing line to %s" % (self.finishingPoint, )
        self.connectedPoints.append(self.lastHighlight + self.finishingPoint)         # concatenates tupples and appends to list
        self.connectionExists = 1
        print '"Real" Point %s, Image Pixel %s' % (self.lastHighlight, self.finishingPoint)

    def save(self):
        print "Writing to file..."
        f = open(self.filename, 'w')
        for point in self.connectedPoints:
            xR = point[0]
            yR = point[1]
            xI = point[2] - self.offsetX     # subtracts offsetX so it saves the image correspondent pixel and not the screen
            yI = point[3]
            f.write('%d,%d,%d,%d\n' % (xR, yR, xI, yI))
        f.close()

        print "Done."

    def updatePts(self):
        for point in self.points_list:
            pygame.draw.circle(self.ptsSurface, POINT_COLOR, point, POINT_RADIUS)
    def updateHighlightedPts(self):
        for highlight in self.highlighted_points:
            pygame.draw.circle(self.highlightSurface, HIGHLIGHT_COLOR, highlight, HIGHLIGHT_RADIUS, HIGHLIGHT_WIDTH)
    def updateLines(self):
        for lines in self.connectedPoints:
            pygame.draw.line(self.highlightSurface, HIGHLIGHT_COLOR, self.lastHighlight, self.finishingPoint, HIGHLIGHT_WIDTH)
    def updateScreen(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.updatePts()
        self.updateHighlightedPts()
        self.updateLines()

        self.screen.blit(self.ptsSurface, (0, 0))               # blits ptsSurface
        self.offsetX = self.ptsSurface.get_rect()[2]            # gets X offset for drawing the image
        self.screen.blit(self.imgSurface, (self.offsetX, 0))    # blits imgSurface to the right of ptsSurface
        self.screen.blit(self.highlightSurface, (0,0))          # blits highlightSurface on the screen

        pygame.display.flip()

    def undo(self):
        if (self.connectionExists == 1 or len(self.connectedPoints) > 0):
            print "Last line was: ", self.connectedPoints[-1]

            pygame.draw.line(self.highlightSurface, BLACK, self.lastHighlight, self.finishingPoint, HIGHLIGHT_WIDTH)
            pygame.draw.circle(self.highlightSurface, BLACK, self.lastHighlight, HIGHLIGHT_RADIUS, HIGHLIGHT_WIDTH)

            # The last tuple (line) and last highlighted point was removed from the list.
            del self.connectedPoints[-1]
            del self.highlighted_points[-1]

            # The connection between 2 pts (the last line) was removed.
            self.connectionExists = 0

            # Updates the base and final points to undraw the lines.
            if (len(self.connectedPoints) > 0):
                self.lastHighlight = self.connectedPoints[-1][0:2]
                self.finishingPoint = self.connectedPoints[-1][2:4]

            print "Number of connections: ", len(self.connectedPoints)
        else:
            print "Nothing to remove."

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == KEYUP:
                if event.key == K_ESCAPE: return False
                if event.key == K_RETURN:
                    self.save()
                if event.key == K_z and pygame.key.get_mods() & KMOD_CTRL: # ctrl + z
                    self.undo() # Remove the last highlighted_point from 'highlighted_points' list
            elif event.type == VIDEORESIZE:
                self.resize(event.w, event.h)
            elif event.type == MOUSEBUTTONUP:
                if self.firstclick == 0:
                    self.point_to_highlight = self.checkPoint(event.pos)

                    if self.point_to_highlight is not None:
                        self.addCircle()
                        self.firstclick = 1

                else: # LINE
                    if (self.highlighted_points):
                        if (self.connectionExists == 0):
                            self.finishingPoint = event.pos
                            self.addLine()

                        self.firstclick = 0

                # DEBUGGING:
                if (len(self.connectedPoints) > 0):
                    print "\n===\tConnected pts:"
                    for i, connected in enumerate(self.connectedPoints):
                        print "connectedPoints[%d]: %s", i, connected
                        print "lastHighlight: ", self.lastHighlight
                        print "finishingPoint: ", self.finishingPoint

        return True

    def mainLoop(self):
        while self.events():
            self.updateScreen()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: %s pointsFile.pts imageFile.img fileToWrite" % sys.argv[0]
        sys.exit()

    pc = PointCorrelator(sys.argv[1], sys.argv[2], sys.argv[3])
    pc.mainLoop()
