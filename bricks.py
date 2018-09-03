from config import *
from entities import *

class Brick(object):
	def print_(self):
		if(self.exists):
			if(self.x + 1 < x_):
				self.scene.scene[self.x + 1,self.y] = self.char[0]
			if(self.x >= 0):
				self.scene.scene[self.x,self.y] = self.char[1]
			

	def destroy(self):
		self.exists = False
		os.system("aplay -Nq ./audio/break.wav &")
		#self.scene.bricks.remove(self)



class Empty_Brick(Brick):
	def __init__(self,x,y,scene):
		self.x = x	
		self.y = y
		self.char = [BRICK_EMPTY,BRICK_EMPTY]
		self.scene = scene
		self.exists = True
		self.type = EMPTY
		self.print_()

class Cake_Brick(Brick):
	def __init__(self,x,y,scene):
		self.x = x
		self.y = y
		self.char = [BRICK_TREASURE_LEFT,BRICK_TREASURE_RIGHT]
		self.scene = scene
		self.exists = True
		self.type = TREASURE
		self.print_()

	def destroy(self):
		os.system("aplay -Nq ./audio/bump.wav &")
		self.exists = False
		#new_block = Empty_Brick(self.x,self.y,self.scene)
		self.scene.entities.append(Cake(self.x,self.y - 1,self.scene))
		self.scene.background[self.x,self.y] = BLOCK
		self.scene.background[self.x + 1,self.y] = BLOCK
		#self.scene.bricks.append(new_block)
		#self.scene.bricks.remove(self)

class Coin_Brick(Brick):
	def __init__(self,x,y,scene):
		self.x = x
		self.y = y
		self.char = [BRICK_TREASURE_LEFT,BRICK_TREASURE_RIGHT]
		self.scene = scene
		self.exists = True
		self.type = COIN
		self.print_()

	def destroy(self):
		os.system("aplay -Nq ./audio/bump.wav &")
		self.exists = False
		self.scene.scene[self.x,self.y - 1] = "$"
		self.scene.scene[self.x + 1,self.y - 1] = "$"
		self.scene.background[self.x,self.y] = BLOCK
		self.scene.background[self.x + 1,self.y] = BLOCK
	
