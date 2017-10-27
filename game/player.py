import pygame
import random
import constants
from blocks import Block
from enemy import Enemy

class Player(pygame.sprite.Sprite):

	def __init__(self):
		
		# Call the parent's constructor
		pygame.sprite.Sprite.__init__(self)

		# get image
		self.image = pygame.image.load('pics/bro_jump3.gif').convert()
		self.rect = self.image.get_rect()
		self.image = pygame.transform.scale(self.image , (int(self.rect.width * constants.MARIO_MULTIPLIER) , int(self.rect.height * constants.MARIO_MULTIPLIER)))
		self.rect = self.image.get_rect()
		self.rect.x = constants.PLAYER_START_POS
		self.rect.y = constants.SCREEN_HEIGHT
		
		# speed vector
		self.change_x = 0
		self.change_y = 0

		# state of player
		self.state = 's'		# stop - right - left - jump
		self.pos_state = 's'	# steady - jump - fall
		# prev coordinates
		self.prev_rect_x = 0

		# viewport
		self.end_of_viewport = 1

		# create blocks , remove after testing
		self.block_sprite_list = pygame.sprite.Group()
		self.block1 = Block(250 , 490)
		self.block_sprite_list.add(self.block1)
		self.block2 = Block(800 , 500)
		self.block_sprite_list.add(self.block2)
		self.block3 = Block(1300 , constants.SCREEN_HEIGHT - 90)
		self.block_sprite_list.add(self.block3)

		# for screen stopping
		self.sstop = 0

	def update(self):

		# check if screen gets stopped
		self.sstop = 0

		# update gravity initially
		self.UpdateGravity()
		#print "b = ",self.rect.right , self.rect.left , self.rect.top , self.rect.bottom

		# update x pos 
		if self.end_of_viewport == 1:
			self.rect.x += self.change_x
		else:
			self.rect.x = constants.SCREEN_WIDTH / 2

		# check for border conditions
		# right border
		if self.rect.right > constants.SCREEN_WIDTH:
			self.rect.right = constants.SCREEN_WIDTH
		# left border
		if self.rect.left < 0:
			self.rect.left = 0

		#print "before collsion = " , self.rect.x , self.rect.y
		# check for collision
		self.block_hit_list = pygame.sprite.spritecollide(self, self.block_sprite_list, False)
		#print "prev = " , self.prev_rect_x
		if len(self.block_hit_list) > 0:
		#	print "touching = True"
			for b in self.block_hit_list:
				# border conditions
				#print "change _ X = " , self.change_x
				#print "pos = " ,b.rect.left , self.rect.right
				# right border
				if b.rect.right <= self.rect.left + self.change_x:
					continue
				# left border
				if b.rect.left >= self.rect.right + self.change_x:
					continue
				if self.change_x > 0:
				#	print "came here"
					self.rect.right = b.rect.left
					self.sstop = 1
				elif self.change_x < 0:
					self.rect.left = b.rect.right
					self.sstop = 1
				else:
				#	print "came"
					self.rect.x = self.prev_rect_x
					self.sstop = 1

		#print "after collision = " , self.rect.x , self.rect.y
		# update game
		#print "stop = ",self.sstop
		
		# update y pos
		self.rect.y += self.change_y
		arr = [str(0.35) , str(0.7) , str(1.05)]
		if str(self.change_y) in arr:
			self.pos_state = 's'
			self.image = pygame.image.load('pics/bro_jump0.gif').convert()
		elif self.change_y <= 0.0:
			self.pos_state = 'j'
			self.image = pygame.image.load('pics/bro_jump1.gif').convert()
		elif self.change_y >= 0.0:
			self.pos_state = 'f'
			self.image = pygame.image.load('pics/bro_jump3.gif').convert()

		# check for border conditions
		# top border
		if self.rect.top < 0:
			self.rect.top = 0		
		# bottom land
		if self.rect.bottom > constants.GROUND_HEIGHT:
			self.rect.bottom = constants.GROUND_HEIGHT
			self.change_y = 0

		# check for collision
		self.block_hit_list = pygame.sprite.spritecollide(self, self.block_sprite_list, False)
		if len(self.block_hit_list) > 0:
			#print "touched"
			for b in self.block_hit_list:
				if self.change_y > 0:
					self.rect.bottom = b.rect.top
					self.change_y = 0
				elif self.change_y < 0:
					self.rect.top = b.rect.bottom
					self.change_y = 0

	
		#print "a = ",self.rect.right , self.rect.left , self.rect.top , self.rect.bottom
		# if screen moves i.e screen stopping equals 0
		if self.sstop == 0:
			self.block_sprite_list.update(self.state , self.end_of_viewport)
			#self.enemy_sprite_list.update()
	
		# before leaving
		#print "before leaving = " , self.rect.x, self.rect.y
		self.prev_rect_x = self.rect.x

	def UpdateGravity(self):
		self.change_y += constants.MOV_GRA

	def jump(self):
		# jump if and only if on ground or on blocks
		# if on ground
		if self.rect.bottom == constants.GROUND_HEIGHT:
			self.change_y = constants.MOV_JMP
		else :# if on block
			self.rect.y += 1
			block_hit_list = pygame.sprite.spritecollide(self , self.block_sprite_list , False)
			self.rect.y -= 1
			if(len(block_hit_list) > 0):
				self.change_y = constants.MOV_JMP

	def MoveLeft(self):
		self.change_x = constants.MOV_LEFT

	def MoveRight(self):
		self.change_x = constants.MOV_RIGHT

	def stop(self):
		self.change_x = constants.MOV_STOP
