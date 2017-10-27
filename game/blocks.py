import pygame
import random
import constants

class Block(pygame.sprite.Sprite):

	def __init__(self , ph , pw):

		# Call the parent's constructor
		pygame.sprite.Sprite.__init__(self)

		# frames
		self.frames = []
		self.frame_idx = -1
		self.pos_x = ph
		self.pos_y = pw

		# setup diff images
		self.SetupFrames()

		# load image
		self.image = self.get_image()
		self.rect = self.image.get_rect()
		self.rect.x = ph
		self.rect.y = pw

	def SetupFrames(self):
		self.frames.append('pics/brick1.gif')
		self.frames.append('pics/brick2.gif')

	def get_image(self):
		self.frame_idx = self.frame_idx + 1
		self.frame_idx = self.frame_idx % len(self.frames)
		tmp_image = pygame.image.load(self.frames[self.frame_idx]).convert()
		tmp_rect = tmp_image.get_rect()
		tmp_image = pygame.transform.scale(tmp_image , (int(tmp_rect.width * constants.BRICK_MULTIPLIER) , tmp_rect.height))
		return tmp_image

	def update(self , state , viewport):
		# blocks should move according to mario state
		# blocks should alse move according to viewport

		if state == 'r':
			if viewport == 0:
				self.rect.x += constants.MOV_LEFT
		elif state == 'l':
			if viewport == 0:
				self.rect.x += constants.MOV_RIGHT
