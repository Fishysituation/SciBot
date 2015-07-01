import pygame
import time
from enum import Enum

class Heading(Enum):
	NORTH = 1
	EAST = 2
	SOUTH = 3
	WEST = 4

class BeeBot(pygame.sprite.Sprite):
	def __init__(self,startLogicalPositionY,startLogicalPositionX,board):
		
		self.board = board
		
		self.logicalPositionX = startLogicalPositionX
		self.logicalPositionY = startLogicalPositionY
		
		self.screenLocationX = startLogicalPositionX * board.step
		self.screenLocationY = (board.logicalHeight - startLogicalPositionY - 1) * board.step
		
		self.sprite=pygame.image.load("./img/robot.jpg")
		self.heading = Heading.NORTH
	
	def display(self,screen):
		screen.blit(self.sprite,(self.screenLocationX,self.screenLocationY))
		pygame.display.update()
		
	def move(self,screen):
		##lets move forward/up first
		
		incrStep = 0
		while ( incrStep < self.board.step ):
			self.screenLocationY = self.screenLocationY - 1
			incrStep = incrStep + 1
			self.board.display(screen)
			self.display(screen)
		
		self.logicalPositionY = self.logicalPositionY - 1