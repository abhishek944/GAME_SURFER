import pygame
import random
import constants
import time
from player import Player
from enemy import Enemy
from coins import Coin
from waves import Wave

def main():

	# start pygame
	pygame.init()

	# pygame font
	pygame.font.init()
	font = pygame.font.Font(None , constants.SCORE_FONT_SIZE)

	# screen size
	screen = pygame.display.set_mode(constants.size)

	# background setup
	background_image = pygame.image.load(constants.WORLD).convert()
	bg_image_rect = background_image.get_rect()
	background_image = pygame.transform.scale(background_image , (int(bg_image_rect.width * constants.WORLD_MULTIPLIER) , int(bg_image_rect.height * constants.WORLD_MULTIPLIER)))
	bg_image_rect = background_image.get_rect()	# after expanding

	# water splash
	WaterSplash = pygame.image.load(constants.WATER_SPLASH).convert()
	ws_image_rect = WaterSplash.get_rect()

	# game name
	pygame.display.set_caption(constants.GAME_NAME)

	# player
	player = Player()

	# enemy
	enemy_sprite_list = pygame.sprite.Group()
	enemy = Enemy(int(random.randint(400 , 800)) , 50)

	# coins
	coin_sprite_list = pygame.sprite.Group()
	coin = Coin(int(random.randint(400 , 800)) , 50)
	coin_score = 0

	# wave
	wave_sprite_list = pygame.sprite.Group()
	wave = Wave(constants.GROUND_HEIGHT , constants.SCREEN_WIDTH)

	# complete sprite list group
	all_sprite_list = pygame.sprite.Group()
	all_sprite_list.add(player)			# add player
	#all_sprite_list.add(enemy)			# add enemy

	# is done constant
	done = False

	# clock
	clock = pygame.time.Clock()

	# camera
	camera_x = 0
	camera_y = 0
	"""
	move_x = -1 * constants.PLAYER_START_POS
	temp_x = 0
	L = constants.SCREEN_WIDTH / 2
	R = bg_image_rect.right - L
	"""
	# other constants
	prev_camera_x = camera_x

	# start times
	start_time_bomb = time.time()
	start_time_coin = time.time()
	start_time_wave = time.time()

	# -- Main Program Loop --
	while not done:

		# events
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				done = True
			if done:
				break
			
			# till key is pressed
			if event.type==pygame.KEYDOWN:
				#if event.key == pygame.K_LEFT:
				#	player.MoveLeft()
				if event.key == pygame.K_RIGHT:
					player.MoveRight()
				if event.key == pygame.K_UP:
					player.jump()

			# if key is taken
			if event.type == pygame.KEYUP:
				#if event.key == pygame.K_LEFT and player.change_x < 0:
				#	player.stop() 
				if event.key == pygame.K_RIGHT and player.change_x > 0:
					player.stop()

		# calculating player state
		if player.change_x > 0:
			player.state = 'r'
		elif player.change_x < 0:
			player.state = 'l'
		else:
			player.state = 's'
 
		# infinite scrolling window created
		if abs(camera_x) > constants.SCREEN_WIDTH/2:	# end of viewport
			player.end_of_viewport = 0
			rel_x = (camera_x + (constants.SCREEN_WIDTH/2)) % bg_image_rect.width
			screen.blit(background_image , [rel_x - bg_image_rect.width , camera_y])
			if rel_x < constants.SCREEN_WIDTH:
				screen.blit(background_image , [rel_x , camera_y])
			if player.sstop == 0:	# if screen moves
				camera_x += -1 * player.change_x
		else:
			player.end_of_viewport = 1
			screen.blit(background_image , [0 , camera_y])
			if player.sstop == 0:	# if screen moves
				camera_x += -1 * player.change_x
		
		if abs(camera_x) > 0:	# game starts
			# for bombs
			if time.time() - start_time_bomb >= 6.5:
				start_time_bomb = time.time()
				rn = int(random.randint(300 , 800))
				enemy = Enemy(rn , 50)
				enemy_sprite_list.add(enemy)

			# for coins
			if time.time() - start_time_coin >= 2.0:
				start_time_coin = time.time()
				rn = int(random.randint(400 , 800))
				coin = Coin(rn , 350)
				coin_sprite_list.add(coin)

			# for waves
			if time.time() - start_time_wave >= 5.0:
				start_time_wave = time.time()
				wave = Wave(constants.SCREEN_WIDTH, constants.GROUND_HEIGHT - 65)
				wave_sprite_list.add(wave)

		# update every sprite list
		all_sprite_list.update()
		enemy_sprite_list.update(player.state , player.end_of_viewport , player.sstop)
		coin_sprite_list.update(player.state , player.end_of_viewport , player.sstop)
		wave_sprite_list.update(player.state , player.end_of_viewport , player.sstop)

		# if bombs off screen - remove
		for enemies in enemy_sprite_list:
			if enemies.rect.y > constants.SCREEN_HEIGHT:
				enemy_sprite_list.remove(enemies)

		# if coins off screen - remove
		for coins in coin_sprite_list:
			if coins.rect.x < 0:
				coin_sprite_list.remove(coins)

		# if waves of screen remove
		for waves in wave_sprite_list:
			if waves.rect.x < 0:
				wave_sprite_list.remove(waves)

		# bombs and player collision detection
		if len(enemy_sprite_list) > 0:
			bullet_hit_list = pygame.sprite.spritecollide(player , enemy_sprite_list , True)
			if len(bullet_hit_list) > 0:
				break

		# coins and player collision
		if len(coin_sprite_list) > 0:
			coin_hit_list = pygame.sprite.spritecollide(player , coin_sprite_list , True)
			coin_score += len(coin_hit_list)

		# waves and player collsion
		if len(wave_sprite_list) > 0:
			wave_hit_list = pygame.sprite.spritecollide(player , wave_sprite_list , False)
			if len(wave_hit_list) > 0:
				break

		# FILL SCREEN
		# blit score
		distance = font.render("Distance = " + str(abs(camera_x)/10) , True , constants.RED , None)
		stars = font.render("Stars = " + str(coin_score) , True , constants.RED , None)
		screen.blit(distance ,[0 , 0])
		screen.blit(stars , [0 , 20])
			
		# blit water splash if and only if he is steady and moving
		if player.pos_state == 's' and player.change_x > 0: 
			ws_image_rect.right = player.rect.left - (player.rect.width / 2)
			ws_image_rect.bottom = player.rect.bottom - (player.rect.height / 2)
			screen.blit(WaterSplash, [ws_image_rect.right , ws_image_rect.bottom])

		# draw everthing
		all_sprite_list.draw(screen)
		player.block_sprite_list.draw(screen)
		enemy_sprite_list.draw(screen)
		coin_sprite_list.draw(screen)
		wave_sprite_list.draw(screen)

		# fps
		clock.tick(60)

		# update screen
		pygame.display.flip()

	# exit pygame
	pygame.quit()

if __name__ == "__main__":
	# call main	
	main()
