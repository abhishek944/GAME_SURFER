import pygame
import random
import constants
from blocks import Block

class Player(pygame.sprite.Sprite):

	def __init__(self):
		
		# Call the parent's constructor
		pygame.sprite.Sprite.__init__(self)

		# block for checking ! Erase if done
		self.image = pygame.image.load('pics/MarioStand.png').convert()
		self.rect = self.image.get_rect()

		# speed vector
		self.change_x = 0
		self.change_y = 0

		# state of player
		self.state = 's'	# stop - right - left - jump

		# viewport
		self.end_of_viewport = 1

		# create blocks
		self.block_sprite_list = pygame.sprite.Group()
		self.block1 = Block(15 , 400 , constants.BLACK , 250 , 490)
		self.block_sprite_list.add(self.block1)

	def update(self):

		# update gravity
		self.UpdateGravity()

		# update x pos if in viewport
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

		# check collision
		block_hit_list = pygame.sprite.spritecollide(self, self.block_sprite_list, False)
		if(len(block_hit_list) > 0):
			for b in self.block_sprite_list:
				if self.change_x > 0:	# if dashed right -> set right = block left
					self.rect.right = b.rect.left
				elif self.change_x < 0:
					self.rect.left = b.rect.right

		# update y pos
		self.rect.y += self.change_y

		# again check collision
		block_hit_list = pygame.sprite.spritecollide(self , self.block_sprite_list , False)
		if(len(block_hit_list) > 0):
			for b in self.block_sprite_list:
				if self.change_y > 0:
					self.rect.bottom = b.rect.top
					self.change_y = 0
				elif self.change_y < 0:
					self.rect.top = b.rect.bottom
					self.change_y = 0

	def UpdateGravity(self):

		# gravity
		self.change_y += constants.MOV_GRA

        # See if we are on the ground.
		if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
			self.change_y = 0
			self.rect.y = constants.SCREEN_HEIGHT - self.rect.height	

	def jump(self):
		# jump if and only if on ground or on blocks

		# if on ground
		if self.rect.bottom == constants.SCREEN_HEIGHT:
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
