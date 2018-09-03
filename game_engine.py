from scene import *
from time import sleep
from beings import *


os.system("aplay -Nq ./audio/start.wav &")
os.system("clear")
username = input("Please input your player name:\n")
scenery = Mountains(username,level = 1)
player1 = Player(5,ground_level - 1,scenery)
cheat_mode = False

while(1 == 1):
	if(player1.score > level_function(scenery.level)):
		scenery.increment_level()
		scenery.its_dragon_time = True
	if(kb.kbhit()):
		insert = kb.getch()
	else:
		insert = NONE

	if(insert == QUIT):
		scenery.print_high_scores(player1.score)
		quit()
	if(insert == "X"):
		cheat_mode = True
		scenery.cheated = True
	if(insert == "e" and cheat_mode):
		player1.eat_cake()
	if(insert == "r" and cheat_mode):
		player1.become_small()
	if(insert == "+" and cheat_mode):
		player1.lives += 1
	
	scenery.move_entities(player1)
	scenery.move_monsters()
	scenery.clear_screen()
	player1.fire(insert)
	scenery.set_bricks()
	scenery.print_entities()
	scenery.print_monsters()
	
	if(player1.isJumping>0):
		player1.isJumping -= 1
	if(insert == UP and player1.isJumping == 0 and player1.isFalling == False):
		if(player1.size == BIG):
			player1.isJumping = 11
		else:
			player1.isJumping = 10
	player1.move(insert,player1.fall_detect(insert))
	
	player1.monster_interact()
	player1.print_char()
	scenery.print_()
	player1.print_stats()
	sleep(dt)