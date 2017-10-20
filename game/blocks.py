import pygame
import random
import constants

class Block(pygame.sprite.Sprite):

	def __init__(self , h , w , c , ph , pw):
		
		# call constructor
		pygame.sprite.Sprite.__init__(self)

		# give image
		self.image = pygame.Surface([w , h])
		self.image.fill(c)
		self.rect = self.image.get_rect()

		# give pos
		self.rect.x = ph
		self.rect.y = pw
	
	def update(self , state , viewport):
		# blocks should move according to mario state
		# blocks should alse move according to viewport

		if state == 'r':
			if viewport == 0:
				self.rect.x += constants.MOV_LEFT
		elif state == 'l':
			if viewport == 0:
				self.rect.x += constants.MOV_RIGHT
