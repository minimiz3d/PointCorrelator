#!/usr/bin/env python

import sys, os
import pygame
from operator import itemgetter
from pygame.locals import *

# Constants
BACKGROUND_COLOR = (250,250,250)
WIDTH, HEIGHT = 640, 480
POINT_COLOR = (0, 150, 0)
POINT_RADIUS = 3

class PointCorrelator(object):
	def __init__(self, pointsFile, imageFile):
		pygame.init()				# initializes pygame modules
		self.pointsFile = pointsFile
		self.imageFile = imageFile
		self.points_list = list()

		self.screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)	# set screen mode
		self.loadPoints()							# loads file with point data
		self.loadImage()							# loads image that the points will be connected to
	
	def loadPoints(self):
		pts = open(self.pointsFile, 'r') 				# opens file with points read-only
		for string in pts.readlines():					# reads file line by line, getting x and y information
			x, y = [int(x) for x in string.split(',')]		# evil string manipulation
			self.points_list.append((x,y)) 				# appends new points to points list
		pts.close()							# close file (good programming!)		
		
		self.ptsSurface = pygame.Surface((max(self.points_list, key=itemgetter(0))[0], \
						max(self.points_list, key=itemgetter(1))[1]))	# creates surface for drawing the points
												# of the size max(x), max(y)

#		self.ptsSurface = pygame.transform.scale(self.ptsSurface, (300, 300)) 		# resize the surface (only resizes the actual
												# surface, not what's drawn into it)
	def loadImage(self):
		self.imgSurface = pygame.image.load(self.imageFile)

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE: return False
			elif event.type == VIDEORESIZE:
				self.resize(event.w, event.h)
		return True

	def resize(self, new_width, new_height):
		self.screen = pygame.display.set_mode((new_width, new_height), RESIZABLE) 	# set new mode for the screen when the window is resized

	def draw(self):
		self.screen.fill(BACKGROUND_COLOR)
		for point in self.points_list:
			pygame.draw.circle(self.ptsSurface, POINT_COLOR, \
						point, POINT_RADIUS)		# draw point by point points in self.points_list (confusing)	
		self.screen.blit(self.ptsSurface, (0, 0)) 			# blits ptsSurface
		offsetX = self.ptsSurface.get_rect()[2]				# gets X offset for drawing the image
		self.screen.blit(self.imgSurface, (offsetX, 0))			# blits imgSurface to the right of ptsSurface
		pygame.display.flip() 						# actually shows shit on screen
	
	def mainLoop(self):
		while self.events():
			self.draw()

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "Usage: %s pointsFile.pts imageFile.img" % sys.argv[0]
		sys.exit()
	
	pc = PointCorrelator(sys.argv[1], sys.argv[2])
	pc.mainLoop()
