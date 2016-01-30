import pickle
import pygame
from src.Obstacle import *
from src.ObstacleGroup import *
from src.Goal import *
from src.GoalGroup import *

class Scenario():

	def __init__(self,name):
				
		self.elements = {}
		self.name = name
		self.elements['Name'] = name
		
		self.switcher = {
			'Name': self.elements['Name'],
		}
		
		self.boardStep = 0
		self.logicalWidth = 0
		self.logicalHeight = 0
		
		self.background = None
		self.borderColour = None
		
		self.beeBotStartPosition = None
		self.beeBotSprite = None
		self.beeBotHeading = None
		
		self.obstacleGroup = {}
		self.obstacleCount = 0

		self.goalGroup = {}
		self.goalCount = 0
		
		self.beeBotFailSprite = None
		
	def get_element(self,key):
	
		if key not in self.elements:
			return None
			
		return self.switcher.get(key)
		
	def setBeeBotFailSprite(self,inputString):
		input = pygame.image.load(inputString)
		self.beeBotFailSprite = self.formatSurfaceForPickle(input)
		
	def getBeeBotFailSprite(self):
		return self.formatPickleToSurface(self.beeBotFailSprite)
	
	def addGoal(self,x,y,sprite=None):
		if sprite != None:
			sprite = pygame.image.load(sprite)
			sprite = self.formatSurfaceForPickle(sprite)
		self.goalGroup[self.goalCount] = (sprite,x,y)
		self.goalCount = self.goalCount + 1
		
	def getGoalGroup(self):
		goalGroup = GoalGroup()
		goalPtr = 0
		while goalPtr < self.goalCount:
			pickledGoal = self.goalGroup[goalPtr]
			goalGroup.add(Goal(self.formatPickleToSurface(pickledGoal[0]),pickledGoal[1],pickledGoal[2],self.boardStep))
			goalPtr = goalPtr + 1
		return goalGroup

	def addObstacle(self,x,y,sprite=None):
		if sprite != None:
			sprite = pygame.image.load(sprite)
			sprite = self.formatSurfaceForPickle(sprite)
		self.obstacleGroup[self.obstacleCount] = (sprite,x,y)
		self.obstacleCount = self.obstacleCount + 1
	
	def getObstacleGroup(self):
		obstacleGroup = ObstacleGroup()
		obsPtr = 0
		while obsPtr < self.obstacleCount:
			pickledObs = self.obstacleGroup[obsPtr]
			obstacleGroup.add(Obstacle(self.formatPickleToSurface(pickledObs[0]),pickledObs[1],pickledObs[2],self.boardStep))
			obsPtr = obsPtr + 1
		return obstacleGroup
		
	def setBeeBotHeading(self,input):
		self.beeBotHeading = input

	def getBeeBotHeading(self):
		return self.beeBotHeading
		
	def setBeeBotSprite(self,inputString):
		input = pygame.image.load(inputString)
		self.beeBotSprite = self.formatSurfaceForPickle(input)
		
	def getBeeBotSprite(self):
		return self.formatPickleToSurface(self.beeBotSprite)
		
	def getBeeBotStartPosition(self):
		return self.beeBotStartPosition
		
	def setBeeBotStartPosition(self,x,y):
		self.beeBotStartPosition = (x,y)
	
	def getLogicalHeight(self):
		return self.logicalHeight
		
	def getLogicalWidth(self):
		return self.logicalWidth	

	def setLogicalHeight(self,input):
		self.logicalHeight = input
		
	def setLogicalWidth(self,input):
		self.logicalWidth = input
		
	def getBoardStep(self):
		return self.boardStep
		
	def setBoardStep(self,input):
		self.boardStep = input
	
	def formatPickleToSurface(self,input):
		if input == None:
			return None
		return pygame.image.fromstring(input['image'],input['size'],input['format'])
	
	def formatSurfaceForPickle(self,input):
		if input == None:
			return None
		return {'image': pygame.image.tostring(input,"RGBA"), 'size': input.get_size(), 'format': "RGBA"}
		
	def setBackground(self,inputString):
		input = pygame.image.load(inputString)
		self.background = self.formatSurfaceForPickle(input)
		
	def getBackground(self):
		return self.formatPickleToSurface(self.background)
		
	def setBorderColour(self,input):
		self.borderColour = input
	
	def getBorderColour(self):
		return self.borderColour
	
	def getName(self):
		return self.elements['Name']
	
	def writeToFile(self):
		pickle.dump( self, open( "./scenarios/"+ self.name +".scibot", "wb" ) )