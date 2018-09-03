import numpy as np 
from config import *
from bricks import *
from beings import *
from os import system
import random
from color import *


class Scene():
	def print_(self):
		system("clear")
		print_game_instructions()
		for i in range(0,y_):
			for j in range(0,x_):
				print(getcolor(self.scene[j,i]),end="")
			print()

	def clear_screen(self):
		new_entities = []
		for i in range(0,len(self.entities)):
			if(self.entities[i].exists):
				new_entities.append(self.entities[i])
		self.entities = new_entities
		new_monsters = []
		for i in range(0,len(self.monsters)):
			if(self.monsters[i].exists):
				new_monsters.append(self.monsters[i])
		self.monsters = new_monsters
		self.scene = np.copy(self.background)

	def set_bricks(self):
		for brick in self.bricks:
			brick.print_()

	def print_monsters(self):
		for monster in self.monsters:
			if(monster.exists):
				monster.print_()

	def move_monsters(self):
		for monster in self.monsters:
			if(monster.exists):
				monster.move()

	def print_entities(self):
		for entity in self.entities:
			entity.print_()

	def game_over(self,score):
		print("Your final score is:",score)
		self.print_high_scores(score)
		os.system("aplay -Nq ./audio/game_over.wav &")
		quit()

	def move_entities(self,player):
		for entity in self.entities:
			if(entity.exists):
				entity.move()
				entity.fall()
				if(entity.exists and  entity.player_captures(player)):
					if(entity.entity_id == 0):
						player.increment_coins()
						entity.exists = False
						player.score += 100
					elif(entity.entity_id == 1):
						player.eat_cake()
						player.score += 100
						entity.exists = False

	def increment_level(self):
		self.level += 1
		self.p_generate_hole = 1 + 5*(self.level - 1)# in 100
		self.prev_generated["Goomba"] += 5 

	def print_high_scores(self,score):
		os.system("clear")
		print("Your score:",score)
		if(self.cheated):
			print("Your name will not be in the list of highest scores, cheater.")
		print("Highscores : ")
		f = open("highscore.txt","r")
		scores = f.readlines()
		if(not self.cheated):
			scores.append(self.playername + " " + ":" + " " + str(score)+ "\n")
		score_list = []
		for i in scores:
			pair = i.split()
			score_list.append(pair)
		for i in score_list:
			i[2] = float(i[2])
		score_list.sort(key = lambda x: x[2],reverse = True)
		for i in score_list:
			i[2] = str(i[2])
		for i in range(0,10):
			print(" ".join(score_list[i]))	
		f = open("highscore.txt", "w")
		for i in range(0,10):
			f.write((" ".join(score_list[i]) + "\n"))			

class Mountains(Scene):
	def __init__(self,playername,level = 1):
		# Setting the stage
		self.level = level
		self.p_generate_hole = 3 + 5*(self.level - 1)# in 100
		self.generate_hole = False
		self.scene = np.array([[BLOCK for i in range(0,y_)] for j in range(0,x_ + 2)])
		self.prev_generated = {"Goomba":3,"Brick":0,"Block":0}
		self.bricks = []
		self.generated_air_bricks = False
		self.entities = []
		self.monsters = []
		self.p_prev_generated_is_coin = 10
		self.gen_height = 0
		self.prev_generated_air_brick = True
		self.generated_ground_bricks = False
		self.generate_coins = 0
		self.coin_height = 6
		self.playername = playername
		self.its_dragon_time = False
		self.cheated = False
		for y in range(3,ground_level):
			self.scene[0:x_,y] = SPACE

		# Generating mountains

		self.mountain_height = 1
		for x in range(1,x_):
			if(self.mountain_height >= 1):
				alpha = ground_level - 1
				beta = ground_level - self.mountain_height
				#self.scene[x,beta:alpha] = MOUNTAIN_TOP
				self.scene[x,beta] = MOUNTAIN_TOP
			a = random.randint(0,1)
			if(a == 0):
				if(self.mountain_height >= 0):
					self.mountain_height -= 1
			else:
				if(self.mountain_height < MAX_MOUNTAIN_HEIGHT):
					self.mountain_height += 1
		self.background = np.copy(self.scene)
		
		#If level is 1, then this generates a predefined first screen.
		if(self.level == 1):
			for i in (39,41,43,45,47):
				if(i != 41 and i != 45):
					self.bricks.append(Empty_Brick(i,y_ - 13,self))
				elif(i == 41):
					self.bricks.append(Cake_Brick(i,y_ - 13,self))
				elif(i == 45):
					self.bricks.append(Coin_Brick(i,y_ - 13,self))


			for i in (41,45):
				self.bricks.append(Coin_Brick(i,y_ - 22,self))

			for i in range(ground_level - 7,ground_level):
				self.bricks.append(Empty_Brick(54,i,self))
				self.bricks.append(Empty_Brick(55,i,self))
				self.bricks.append(Empty_Brick(56,i,self))
				self.bricks.append(Empty_Brick(57,i,self))
				self.bricks.append(Empty_Brick(58,i,self))


			for i in range(65,71):
				self.entities.append(Coin(i,ground_level - 2,self))
			self.monsters.append(Goomba(49,ground_level - 1,self))
			self.monsters.append(Goomba(51,ground_level- 1,self))
			#self.monsters.append(Dragon(x_ - 10,ground_level - 1,self))



	def next_generate(self):
		# Function to generate the next block of area after the player has arrived at middle portion of the screen.

		# Shift screen to the left

		for i in range(1,x_):
			self.background[i - 1,0:y_] = self.background[i,0:y_]

		for y in range(4,ground_level - 1):
			self.background[x_ - 1,y] = SPACE
		self.background[x_ - 1,0:3] = BLOCK 
		self.background[x_ - 1,ground_level :y_] = BLOCK 

		# Move current bricks,entities and enemies one step back
		
		for brick in self.bricks:
			if(brick.x == -1):
				brick.exists = False
			else:
				brick.x -= 1
		
		for entity in self.entities:
			if(entity.x == -1):
				entity.exists = False
			else:
				entity.x -= 1

		for monster in self.monsters:
			if(monster.x == -1):
				monster.exists = False
			else:
				monster.x -= 1
		
		# Generate the mountains and other stuff for the next block.

		a = random.randint(0,1)
		if(self.mountain_height > 0):
			self.background[x_ - 1,ground_level - self.mountain_height] = SPACE
		if(a == 0):
			if(self.mountain_height >= 0):
				self.mountain_height -= 1
		else:
			if(self.mountain_height < MAX_MOUNTAIN_HEIGHT):
				self.mountain_height += 1
		if(self.mountain_height >= 1):
			self.background[x_ - 1,ground_level - self.mountain_height] = MOUNTAIN_TOP	

		
		# Generating the ground level bricks for the next blocks.
		
		if(not self.generated_ground_bricks):
			p = random.randint(1,100)
			if(p <= self.p_generate_hole or self.generate_hole):
				self.generated_ground_bricks = True
				if(self.generate_hole):
					self.generate_hole = False
				else:
					self.generate_hole = True
				for i in range(0,y_):
					self.background[x_ - 1,i] = SPACE

		if(not self.generated_ground_bricks):
			self.generated_ground_bricks = True
		#	self.gen_height += random.choice(p_dist_bricks)
			self.gen_height = random.choice(p_dist_bricks)
			if(self.gen_height > 20):
				self.gen_height = 20
			if(self.gen_height < 0):
				self.gen_height = 0
			for i in range(ground_level - self.gen_height,ground_level):
				self.bricks.append(Empty_Brick(x_ - 1,i,self))

		else:
			self.generated_ground_bricks  = False

		# Generating treasure bricks and other bricks that are present in the air.

		if(not self.generated_air_bricks):
			if(not self.prev_generated_air_brick):
				p = random.randint(0,50)
			else:
				p = random.randint(1,10)
			if(p < 6):
				g = random.randint(0,100)
				if(g <= self.p_prev_generated_is_coin):
					self.bricks.append(Coin_Brick(x_ - 1, ground_level - height_air_bricks,self))
					self.p_prev_generated_is_coin = 40
				elif(g > 97):
					self.bricks.append(Cake_Brick(x_ - 1, ground_level - height_air_bricks,self))
					self.p_prev_generated_is_coin = 40
				else:
					self.bricks.append(Empty_Brick(x_ - 1, ground_level -  height_air_bricks,self))
					self.p_prev_generated_is_coin = 10
				g = random.randint(1,100)
				self.generated_air_bricks = True
				self.prev_generated_air_brick = True
			else:
				self.prev_generated_air_brick = False
		else:
			self.generated_air_bricks = False

		# Generating coins

		if(random.randint(1,100) < p_generate_coin):
			self.generate_coins = random.randint(1,5)

		if(self.generate_coins > 0):
			if(self.generate_coins % 2 == 0):
				self.entities.append(Coin(x_ - 1,ground_level - self.coin_height - 1,self))
			else:
				self.entities.append(Coin(x_ - 1,ground_level - self.coin_height,self))
			self.generate_coins -= 1
		# Generating goombas and chains of goombas
		if(not self.its_dragon_time):
			p = random.randint(1,100)
			if(p <= self.prev_generated["Goomba"]):
				self.monsters.append(Goomba(x_ - 2,ground_level - self.gen_height - 25,self))
				g = random.randint(1,100)
				if(g <= 10):
					self.monsters.append(Goomba(x_ - 4,ground_level - self.gen_height - 25,self))
					g = random.randint(1,100)
					if(g <= 5):
						g = random.randint(1,100)
						self.monsters.append(Goomba(x_ - 6,ground_level - self.gen_height - 25,self))
						if(g == 1):
							self.monsters.append(Goomba(x_ - 8,ground_level - self.gen_height - 25,self))

		else:
			self.monsters.append(Dragon(x_ - 10,ground_level - 1,self))
			self.its_dragon_time = False