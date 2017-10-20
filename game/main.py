import pygame
import random
import constants
from player import Player

def main():

	# start pygame
	pygame.init()

	# screen size
	screen = pygame.display.set_mode(constants.size)

	# background setup
	background_image = pygame.image.load(constants.WORLD).convert()
	bg_image_rect = background_image.get_rect()
	background_image = pygame.transform.scale(background_image , (int(bg_image_rect.width * constants.WORLD_MULTIPLIER) , int(bg_image_rect.height * constants.WORLD_MULTIPLIER)))
	bg_image_rect = background_image.get_rect()	# after expanding

	# game name
	pygame.display.set_caption(constants.GameName)

	# player
	player = Player()

	# complete sprite list group
	all_sprite_list = pygame.sprite.Group()
	all_sprite_list.add(player)			# add player

	# is done constant
	done = False

	# clock
	clock = pygame.time.Clock()

	# camera
	camera_x = 0
	camera_y = 0
	move_x = 0
	temp_x = 0
	L = constants.SCREEN_WIDTH / 2
	R = bg_image_rect.right - L

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
				if event.key == pygame.K_LEFT:
					player.MoveLeft()
				if event.key == pygame.K_RIGHT:
					player.MoveRight()
				if event.key == pygame.K_UP:
					player.jump()

			# if key is taken
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT and player.change_x < 0:
					player.stop() 
				if event.key == pygame.K_RIGHT and player.change_x > 0:
					player.stop()

		# calculating player state
		if player.change_x > 0:
			player.state = 'r'
		elif player.change_x < 0:
			player.state = 'l'
		else:
			player.state = 's'

		# camera position calculation
		move_x += -1 * player.change_x	# bg moves opposite to player
		temp_x = abs(move_x)
		if temp_x < L:			# world : [...L..............................R...]
			temp_x = -1 * L 	# camera movement from [0 to R - L] 
		elif temp_x > R:
			temp_x = -1 * R
		else:
			temp_x = move_x

		camera_x = temp_x + L
		if camera_x == 0 or camera_x == L-R:
			player.end_of_viewport = 1
		else:
			player.end_of_viewport = 0

		#print player.rect.x , player.rect.y , camera_x , player.end_of_viewport
		# fill screen
		screen.fill(constants.WHITE)
		screen.blit(background_image , [camera_x , camera_y])
		
		# to avoid some starting game glitch 
		# donno glitch
		if abs(camera_x) >= 0 and abs(camera_x) <= L and player.rect.x > L:
			player.rect.x = L

		# update every sprite list
		all_sprite_list.update()
		player.block_sprite_list.update(player.state , player.end_of_viewport)

		# draw everthing - should be above clock
		all_sprite_list.draw(screen)
		player.block_sprite_list.draw(screen)

		# fps
		clock.tick(60)

		# update screen
		pygame.display.flip()

	# exit pygame
	pygame.quit()
		

if __name__ == "__main__":
	# call main	
	main()
