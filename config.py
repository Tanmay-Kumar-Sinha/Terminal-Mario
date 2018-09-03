# For non blocking input

from NonBlockingInput import *
kb = KBHit()

# Global time step

dt = 1/50

# Variables and lists for probabilities.

p_dist_bricks = [0]*500 + [1]*25 + [2]*10 + [3]*25 + [4]*20   
p_prev_generated_is_coin = 10
p_generate_coin = 5 

# Length of game area, full screen length of terminal, and other variables related to the envionment. 

x_length = 168
y_length = 50
x_ = 3*x_length//5
y_ = 7*y_length//8
ground_level = y_ - 5
MAX_MOUNTAIN_HEIGHT = 30
SMALL = 0
BIG = 1
PLAYER = 1

COIN = 2
TREASURE = 1
EMPTY = 0
height_air_bricks = 9
# keypress mappings

QUIT = "q"
LEFT = "a"
RIGHT = "d"
UP = "w"
DOWN = "s"
NONE = "p"
FIRE_KEY = "f"

# unicode characters to be printed

BLOCK = u'\U00002592'#u'\U00002588'
SPACE = " "

MOUNTAIN_TOP = "^"
MOUNTAIN_INCREASE = '/'
MOUNTAIN_DECREASE = '\\'


MARIO_BODY_PARTS = []
MARIO_LEFT_LEG_1 = u'\U000023a0'
MARIO_BODY_PARTS.append(MARIO_LEFT_LEG_1) 
MARIO_RIGHT_LEG_1 = u'\U0000239d'
MARIO_BODY_PARTS.append(MARIO_RIGHT_LEG_1)
MARIO_RIGHT_CHEST_1 = u'\U0000258f'
MARIO_BODY_PARTS.append(MARIO_RIGHT_CHEST_1) 
MARIO_LEFT_CHEST_1 = u'\U00002595'
MARIO_BODY_PARTS.append(MARIO_LEFT_CHEST_1) 
MARIO_LEFT_ARM_1 = "/"
MARIO_BODY_PARTS.append(MARIO_LEFT_ARM_1) 
MARIO_RIGHT_ARM_1 = "\\"
MARIO_BODY_PARTS.append(MARIO_RIGHT_ARM_1) 
MARIO_LEFT_HEAD_1 =  u'\U000025A1'#u'\U00002b57'
MARIO_BODY_PARTS.append(MARIO_LEFT_HEAD_1) 
MARIO_RIGHT_HEAD_1 =  u'\U000025A1'#u'\U00002b57'
MARIO_BODY_PARTS.append(MARIO_RIGHT_HEAD_1)

MARIO_LEFT_LEG_2 = u'\U000023a0'#u'\U000023a6'
MARIO_BODY_PARTS.append(MARIO_LEFT_LEG_2) 
MARIO_RIGHT_LEG_2 = u'\U0000239d'#u'\U000023a3'
MARIO_BODY_PARTS.append(MARIO_RIGHT_LEG_2) 
MARIO_LEFT_ABDOMEN_2 = u'\U00002595'#u'\U000023a9'
MARIO_BODY_PARTS.append(MARIO_LEFT_ABDOMEN_2) 
MARIO_RIGHT_ABDOMEN_2 = u'\U0000258f'#u'\U000023ad'
MARIO_BODY_PARTS.append(MARIO_RIGHT_ABDOMEN_2) 
MARIO_RIGHT_CHEST_2 = "\\"#u'\U000023ab'
MARIO_BODY_PARTS.append(MARIO_RIGHT_CHEST_2) 
MARIO_LEFT_CHEST_2 = "/"#u'\U000023a7'
MARIO_BODY_PARTS.append(MARIO_LEFT_CHEST_2) 
MARIO_LEFT_ARM_2 = "/"
MARIO_BODY_PARTS.append(MARIO_LEFT_ARM_2) 
MARIO_RIGHT_ARM_2 = "\\"
MARIO_BODY_PARTS.append(MARIO_RIGHT_ARM_2) 
MARIO_LEFT_HEAD_2 = u'\U000025A1' #u'\U00002b57'
MARIO_BODY_PARTS.append(MARIO_LEFT_HEAD_2) 
MARIO_RIGHT_HEAD_2 = u'\U000025A1' #u'\U00002b57'
MARIO_BODY_PARTS.append(MARIO_RIGHT_HEAD_2) 

MARIO_HAT_LEFT = u'\U0000259f'
MARIO_BODY_PARTS.append(MARIO_HAT_LEFT) 
MARIO_HAT_RIGHT = u'\U00002599'
MARIO_BODY_PARTS.append(MARIO_HAT_RIGHT) 

GOOMBA_LEFT = u'\U0000259b'
GOOMBA_RIGHT = u'\U0000259C'

FIREBALL = u'\U00002126'

COIN_CHAR = u'\U00002689'
CAKE = u'\U00002135'
BRICK_EMPTY = u'\U00002588'
BRICK_TREASURE_LEFT = u'\U00001450'#"x" 
BRICK_TREASURE_RIGHT = u'\U00001455'#"x" 
OPAQUE_BLOCKS = [BRICK_TREASURE_LEFT,BRICK_TREASURE_RIGHT,BRICK_EMPTY,BLOCK]
TRANSPARENT_BLOCKS = [SPACE,MOUNTAIN_TOP,COIN_CHAR,CAKE,GOOMBA_RIGHT,GOOMBA_LEFT,FIREBALL]
TREASURE_BLOCKS = [BRICK_TREASURE_RIGHT,BRICK_TREASURE_LEFT]
ENEMY_PARTS = [GOOMBA_RIGHT,GOOMBA_LEFT]


DRAGON_PARTS = [u'\U0000259c',u'\U0000259b',u'\U00002590',u'\U0000258b',u'\U00002593',u'\U00002593',u'\U00002583',u'\U00002207']

for i in MARIO_BODY_PARTS:
	TRANSPARENT_BLOCKS.append(i)
for i in DRAGON_PARTS:
	TRANSPARENT_BLOCKS.append(i)
	ENEMY_PARTS.append(i)
# Functions to write instructions.

def print_game_instructions():
	print("W: Jump",end="\t\t\t")
	print("A: Move Left")
	print("D: Move Right",end="\t\t")
	print("F: Throw fireball")


# Function to change level according to score.

def level_function(level):
	if(level == 1):
		return 10000
	elif(level == 2):
		return 25000
	elif(level == 3):
		return 40000
	elif(level == 4):
		return 60000
	elif(level == 5):
		return 100000
	else:
		return 100000*(level - 4)