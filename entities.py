from config import *


class Entity():
	def move(self):
		return 

	def fall(self):
		return 

	def player_captures(self,player):
		return 

class Cake(Entity):
	def __init__(self,x,y,scene):
		self.x = x
		self.y = y
		self.scene = scene
		scene.entities.append(self)
		self.move_dir = RIGHT
		self.exists = True
		self.print_()
		self.moved = 0
		self.entity_id = 1

	def move(self):
		self.moved += 1
		if(self.move_dir == RIGHT):
			if(self.x + 2 >= x_):
				self.exists = False
				return
			if(self.scene.scene[self.x + 2,self.y] in TRANSPARENT_BLOCKS):
				if(self.moved % 5 == 0):
					self.x += 1
			else:
				self.move_dir = LEFT
		elif(self.move_dir == LEFT):
			if(self.x -1 < 0):
				self.exists = False
			if(self.scene.scene[self.x - 1,self.y] in TRANSPARENT_BLOCKS):
				if(self.moved % 5 == 0):
					self.x -= 1
			else:
				self.move_dir = RIGHT

	def fall(self):
		if(self.scene.scene[self.x,self.y + 1] in TRANSPARENT_BLOCKS and self.scene.scene[self.x + 1,self.y + 1] in TRANSPARENT_BLOCKS):
			self.y += 1 
		if(self.y >= y_ - 1):
				self.exists = False

	def player_captures(self,player):
		if(player.size == SMALL):
			if(((self.x >= player.x and self.x <= player.x + 1) and (self.y <= player.y  and self.y >= player.y - 3) or
				(self.x + 1 >= player.x and self.x + 1<= player.x + 1) and (self.y <= player.y  and self.y >= player.y - 3))):
				return True
			else:
				return False
		elif(player.size == BIG):
			if(((self.x >= player.x and self.x <= player.x + 1) and (self.y <= player.y  and self.y >= player.y - 4) or
				(self.x + 1 >= player.x and self.x + 1<= player.x + 1) and (self.y <= player.y  and self.y >= player.y - 4))):
				return True
			else:
				return False
			

	def print_(self):
		if(self.exists):
			if(self.x >= 0):
				self.scene.scene[self.x,self.y] = CAKE
			if(self.x + 1 < x_):
				self.scene.scene[self.x + 1,self.y] = CAKE

class Coin(Entity):
	def __init__(self,x,y,scene):
		self.scene = scene
		self.exists = True
		self.x = x
		self.y = y
		self.char = COIN_CHAR
		self.entity_id = 0

	def player_captures(self,player):
		if(player.size == SMALL):
			if((self.x >= player.x and self.x <=player.x + 1) and (self.y >= player.y - 3 and self.y <= player.y)):
				return True
			else:
				return False
		else:
			if((self.x >= player.x and self.x <=player.x + 1) and (self.y >= player.y - 4 and self.y <= player.y)):
				return True
			else:
				return False

	def print_(self):
		if(self.exists):
			self.scene.scene[self.x,self.y] = self.char

class FireBall(Entity):
	def __init__(self,x,y,scene,player):
		self.x = x
		self.y = y
		self.scene = scene
		self.char = FIREBALL
		self.exists = True
		self.moved = 0
		self.player = player

	def print_(self):
		self.scene.scene[self.x,self.y] = self.char

	def move(self):
		if(self.x > x_ - 1):
			self.exists = False
			return
		if(self.x < 0):
			self.exists = False
			return
		new_x = self.x + 1
		if(self.y + 1 >= y_):
			self.exists = False
			return
		if(self.scene.scene[self.x + 1,self.y + 1] in TRANSPARENT_BLOCKS):
			new_y = self.y + 1
		else:
			new_y = self.y - 1
		if(self.scene.scene[new_x,new_y] in ENEMY_PARTS):
			for monster in self.scene.monsters:
				if(monster.monster_id == 0):
					if((monster.x == new_x or monster.x + 1 == self.x) and monster.y == new_y):
						monster.die()
						self.player.score += 200*self.scene.level
				elif(monster.monster_id == 1):
					coods =(new_x,new_y)
					if(coods == (monster.x,monster.y) or coods == (monster.x - 1,monster.y - 1) or coods == (monster.x - 1,monster.y - 2) or 
						coods == (monster.x,monster.y - 1) or coods == (monster.x,monster.y - 2) or coods == (monster.x + 1,monster.y - 2)):
						monster.die()
						self.player.score += 100*self.scene.level
			self.exists = False
			return

		if(self.scene.scene[new_x,new_y] not in TRANSPARENT_BLOCKS):
			self.exists = False
		else:
			self.x = new_x
			self.y = new_y
			self.moved += 1
