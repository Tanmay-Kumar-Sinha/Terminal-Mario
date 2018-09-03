from config import *
from entities import *
import numpy as np
from bricks import *

class Being():
	def move(self,direction_x,direction_y):
		if(direction_y == UP):
			self.y -= 1
		elif(direction_y == DOWN):
			self.y += 1
		if(direction_x == RIGHT):
			self.x += 1
		elif(direction_x == LEFT):
			self.x -= 1


	def fall_detect(self,insert):
		if(self.isJumping > 0):
			return UP
		if(self.scene.scene[self.x,self.y + 1] in TRANSPARENT_BLOCKS and self.scene.scene[self.x + 1,self.y + 1] in TRANSPARENT_BLOCKS):
			self.isFalling = True
			return DOWN
		else:
			self.isFalling = False
			return insert

	def die(self):
		self.exists = False

class Player(Being):
	def __init__(self,x,y,scene):
		self.x = x
		self.y = y
		self.scene = scene
		self.size = SMALL
		self.type = PLAYER
		self.print_char()
		self.isJumping = 0
		self.isFalling = False
		self.score = 0
		self.coins = 0
		self.lives = 3
		self.height = 3
		self.has_fire_ability = False

	def eat_cake(self):
		if(self.size == SMALL):
			self.size = BIG
			self.height = 4
			self.score += 200*self.scene.level
			os.system("aplay -Nq ./audio/eat_cake.wav &")
		else:
			self.has_fire_ability = True

	def fire(self,insert):
		if(self.has_fire_ability and insert == FIRE_KEY):
			self.scene.entities.append(FireBall(self.x + 2,self.y,self.scene,self))

	def become_small(self):
		self.size = SMALL
		self.has_fire_ability = False

	def print_stats(self):
		print("SCORE=",self.score)
		print("COINS=",self.coins)
		print("LIVES=",self.lives)

	def increment_coins(self):
		self.score += 100*self.scene.level
		if(self.coins == 99):
			self.lives += 1
			self.coins = 0
			os.system("aplay -Nq ./audio/1up.wav &")

		else:
			self.coins += 1

	def die(self,certainty):
		self.has_fire_ability = False
		os.system("aplay -Nq ./audio/death.wav &")
		if(certainty == 1):
			self.size = SMALL
		if(self.size == BIG):
			self.become_small()
		else:
			if(self.lives > 0):
				self.lives -= 1
				self.x = 5
				self.y = ground_level - 20
			else:
				self.scene.game_over(self.score)


	def monster_interact(self):
		for monster in self.scene.monsters:
			if(monster.monster_id == 0):
				if((monster.x == self.x or monster.x == self.x + 1 or monster.x + 1 == self.x) and (monster.y >= self.y - self.height and monster.y <= self.y)):
					self.die(0)
					monster.die()
				elif((monster.x == self.x or monster.x == self.x + 1 or monster.x + 1 == self.x) and (monster.y == self.y + 1)):
					monster.die()
					self.score += 200*self.scene.level
			elif(monster.monster_id == 1):
				if((monster.x - 1 == self.x + 1) and self.y == monster.y):
					self.die(0)
	def print_char(self):
		if(self.size == BIG):
			self.scene.scene[self.x,self.y] = MARIO_LEFT_LEG_2
			self.scene.scene[self.x + 1,self.y] = MARIO_RIGHT_LEG_2
			self.scene.scene[self.x,self.y - 1] = MARIO_LEFT_ABDOMEN_2
			self.scene.scene[self.x + 1,self.y - 1] = MARIO_RIGHT_ABDOMEN_2
			self.scene.scene[self.x + 1,self.y - 2] = MARIO_RIGHT_CHEST_2
			self.scene.scene[self.x,self.y - 2] = MARIO_LEFT_CHEST_2
			#self.scene.scene[self.x - 1,self.y -2] = MARIO_LEFT_ARM_2
			#self.scene.scene[self.x + 2,self.y -2] = MARIO_RIGHT_ARM_2
			self.scene.scene[self.x,self.y - 3] = MARIO_LEFT_HEAD_2
			self.scene.scene[self.x + 1,self.y - 3] = MARIO_RIGHT_HEAD_2
			self.scene.scene[self.x,self.y - 4] = MARIO_HAT_LEFT
			self.scene.scene[self.x + 1,self.y - 4] = MARIO_HAT_RIGHT
		else:
			self.scene.scene[self.x,self.y] = MARIO_LEFT_LEG_1
			self.scene.scene[self.x + 1,self.y] = MARIO_RIGHT_LEG_1
			self.scene.scene[self.x + 1,self.y - 1] = MARIO_RIGHT_CHEST_1
			self.scene.scene[self.x,self.y - 1] = MARIO_LEFT_CHEST_1
			#self.scene.scene[self.x - 1,self.y - 1] = MARIO_LEFT_ARM_1
			#self.scene.scene[self.x + 2,self.y - 1] = MARIO_RIGHT_ARM_1
			self.scene.scene[self.x,self.y - 2] = MARIO_LEFT_HEAD_1
			self.scene.scene[self.x + 1,self.y - 2] = MARIO_RIGHT_HEAD_1
			self.scene.scene[self.x,self.y - 3] = MARIO_HAT_LEFT
			self.scene.scene[self.x + 1,self.y - 3] = MARIO_HAT_RIGHT

	def collision_detector(self,direction):
		if(direction == RIGHT):
			if(self.size == SMALL):
				if(self.scene.scene[self.x + 2,self.y] in TRANSPARENT_BLOCKS and self.scene.scene[self.x + 2,self.y - 1] in TRANSPARENT_BLOCKS
					and self.scene.scene[self.x + 2,self.y - 2] in TRANSPARENT_BLOCKS and self.scene.scene[self.x + 2,self.y - 3] in TRANSPARENT_BLOCKS):
					return False
				else:
					return True
			else:
				if(self.scene.scene[self.x + 2,self.y] in TRANSPARENT_BLOCKS and self.scene.scene[self.x + 2,self.y - 1] in TRANSPARENT_BLOCKS
						and self.scene.scene[self.x + 2,self.y - 2] in TRANSPARENT_BLOCKS and self.scene.scene[self.x + 2,self.y - 3] in TRANSPARENT_BLOCKS
						and self.scene.scene[self.x + 2,self.y - 4] in TRANSPARENT_BLOCKS):
					return False
				else:
					return True

		elif(direction == LEFT):
			if(self.size == SMALL):
				if(self.scene.scene[self.x - 1,self.y] in TRANSPARENT_BLOCKS and self.scene.scene[self.x - 1,self.y - 1] in TRANSPARENT_BLOCKS
					and self.scene.scene[self.x - 1,self.y - 2] in TRANSPARENT_BLOCKS and self.scene.scene[self.x - 1,self.y - 3] in TRANSPARENT_BLOCKS):
					return False
				else:
					return True
			else:
				if(self.scene.scene[self.x - 1,self.y] in TRANSPARENT_BLOCKS and self.scene.scene[self.x - 1,self.y - 1] in TRANSPARENT_BLOCKS
					and self.scene.scene[self.x - 1,self.y - 2] in TRANSPARENT_BLOCKS and self.scene.scene[self.x - 1,self.y - 3] in TRANSPARENT_BLOCKS and 
						self.scene.scene[self.x - 1,self.y - 4] in TRANSPARENT_BLOCKS):
						return False
				else:
						return True

		elif(direction == UP):
			if(self.size == SMALL):
				if(self.scene.scene[self.x,self.y - 4] in TRANSPARENT_BLOCKS and self.scene.scene[self.x + 1,self.y - 4]
				in TRANSPARENT_BLOCKS):
					return False
				else:
					return True
			else:
				if(self.scene.scene[self.x,self.y - 5] in TRANSPARENT_BLOCKS and self.scene.scene[self.x + 1,self.y - 5] in TRANSPARENT_BLOCKS):
					return False
				else:
					return True

		elif(direction == DOWN):
			if(self.scene.scene[self.x,self.y + 1] in TRANSPARENT_BLOCKS and self.scene.scene[self.x + 1,self.y + 1] in TRANSPARENT_BLOCKS):
				return False
			else:
				return True

	def move(self,direction_x,direction_y):
		if(direction_x == LEFT):				
			if(self.x != 0):
				if(not self.collision_detector(direction_x)):
					self.x -= 1


		elif(direction_x == RIGHT):
			if(self.x == int(x_/2)):
				if(not self.collision_detector(RIGHT)):
						self.scene.next_generate()
			else:
				if(not self.collision_detector(RIGHT)):
						self.x += 1


		if(direction_y == UP):
			if(self.size == SMALL):
				if(not self.collision_detector(direction_y)):
					self.y -= 1
				else:
					os.system("aplay -Nq ./audio/bump.wav &")
					self.isJumping = 0
					if(self.scene.scene[self.x,self.y - 4] in TREASURE_BLOCKS):
						for brick in self.scene.bricks:
							if((brick.x == self.x or brick.x == self.x + 1 or brick.x + 1 == self.x or brick.x + 1 == self.x + 1) and (brick.y == self.y - 4)
								and brick.exists):
								if(brick.type == TREASURE):
									brick.destroy()
									self.score += 100*self.scene.level
								elif(brick.type == COIN):
									brick.destroy()
									self.score += 200*self.scene.level
									self.increment_coins()

			else:
				if(not self.collision_detector(direction_y)):
					self.y -= 1
				else:
					broken = False
					if(self.isJumping > 0):
						for brick in self.scene.bricks:
							if((brick.x == self.x or brick.x == self.x + 1 or brick.x + 1 == self.x or brick.x + 1 == self.x + 1) and (brick.y == self.y - 5)
								and brick.exists and not broken):
								brick.destroy()
								self.score += 100*self.scene.level
								broken = True
								if(brick.type == COIN):
									self.increment_coins()
					self.isJumping = 0
	
		elif(direction_y == DOWN):
			if(not self.collision_detector(direction_y)):
				self.y += 1
			if(self.y >= y_ - 1):
				self.die(1)

class Goomba(Being):
	def __init__(self,x,y,scene):
		self.x = x
		self.y = y
		self.scene = scene
		self.exists = True
		self.move_dir = LEFT
		self.moved = 0
		self.monster_id = 0

	def print_(self):
		if(self.exists):
			if(self.x >= 0):
				self.scene.scene[self.x,self.y] = GOOMBA_LEFT
			if(self.x + 1 < x_):
				self.scene.scene[self.x + 1,self.y] = GOOMBA_RIGHT

	def collision_detector(self,direction):
		if(direction == LEFT):
			if(self.x >= 0 and self.scene.scene[self.x - 1,self.y] in TRANSPARENT_BLOCKS):
				return False
			else:
				return True

		elif(direction == RIGHT):
			if(self.scene.scene[self.x + 2,self.y] in TRANSPARENT_BLOCKS):
				return False
			else:
				return True

		elif(direction == DOWN):
			if(self.scene.scene[self.x,self.y + 1] in TRANSPARENT_BLOCKS and self.scene.scene[self.x + 1,self.y + 1] in TRANSPARENT_BLOCKS):
				return False
			else:
				return True

	def die(self):
		self.exists = False
		os.system("aplay -Nq ./audio/stomp.wav &")


	def move(self):
		invert = False
		direction = self.move_dir
		if(self.x == 0 and self.move_dir == LEFT):
			self.exists = False
		if(self.x == x_ - 2 and self.move_dir == RIGHT):
			self.exists = False
		self.moved += 1
		if(self.scene.level > 5):
			m = 5
		else:
			m = self.scene.level
		if(self.moved % (6 - m) == 0):
			if(direction == RIGHT):
				if(not self.collision_detector(RIGHT)):
					self.x += 1
				else:
					self.move_dir = LEFT
			elif(direction == LEFT):
				if(not self.collision_detector(LEFT)):
					self.x -= 1
				else:
					self.move_dir = RIGHT

		if(not self.collision_detector(DOWN)):
			self.y += 1
			if(self.y >= y_ - 1):
				self.die()

class Dragon(Being):
	def __init__(self,x,y,scene):
		self.x = x
		self.y = y
		self.scene = scene
		self.exists = True
		self.scene.bricks.append(Cake_Brick(self.x - 10,self.y - 5,self.scene))
		self.scene.bricks.append(Cake_Brick(self.x - 12,self.y - 5,self.scene))
		self.health = 10
		self.spawn_enemy = 1
		self.monster_id = 1

	def print_(self):
		self.scene.scene[self.x,self.y] = DRAGON_PARTS[0]
		self.scene.scene[self.x + 1,self.y] = DRAGON_PARTS[1]
		self.scene.scene[self.x,self.y - 1] = DRAGON_PARTS[2]
		self.scene.scene[self.x + 1,self.y - 1] = DRAGON_PARTS[3]
		self.scene.scene[self.x,self.y - 2] = DRAGON_PARTS[4]
		self.scene.scene[self.x + 1,self.y - 2] = DRAGON_PARTS[5]
		self.scene.scene[self.x - 1,self.y - 2] = DRAGON_PARTS[6]
		self.scene.scene[self.x - 1,self.y - 1] = DRAGON_PARTS[7]

	def move(self):
		if(self.x <= 0):
			self.exists = False
			return
		if(self.spawn_enemy % 100 == 0):
			self.scene.monsters.append(Goomba(self.x - 1,self.y ,self.scene))
		self.spawn_enemy += 1


	def die(self):
		if(self.health < 0):
			self.exists = False
		else:
			self.health -= 1