from config import *

colors = {
    'Black'            : '\x1b[1;30m',
    'Blue'             : '\x1b[1;94m',
    'Green'            : '\x1b[1;92m',
    'Cyan'             : '\x1b[0;36m',
    'Red'              : '\x1b[0;31m',
    'Purple'           : '\x1b[0;35m',
    'Brown'            : '\x1b[0;33m',
    'Gray'             : '\x1b[0;37m',
    'Dark Gray'        : '\x1b[1;30m',
    'Light Blue'       : '\x1b[1;34m',
    'Light Cyan'       : '\x1b[1;36m',
    'Light Red'        : '\x1b[1;31m',
    'Light Purple'     : '\x1b[1;35m',
    'Yellow'           : '\x1b[1;33m',
    'White'            : '\x1b[1;37m'
}

def getcolor(charac):

	if(charac == COIN_CHAR or charac == "$"):
		color = "Yellow"
	elif(charac == BRICK_EMPTY):
		color = "Red"
	elif(charac == BLOCK):
		color = "Light Blue"
	elif(charac == MOUNTAIN_TOP):
		color = "Green"
	elif(charac == BRICK_TREASURE_LEFT or charac == BRICK_TREASURE_RIGHT):
		color = "Yellow"
	elif(charac == GOOMBA_LEFT or charac == GOOMBA_RIGHT):
		color = "Gray"
	elif(charac in MARIO_BODY_PARTS):
		color = "White"
	elif(charac == FIREBALL):
		color = "Yellow"
	else:
		color = "White"
	return(colors[color]+charac+'\x1b[0m')