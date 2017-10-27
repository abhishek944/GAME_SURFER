import pygame
import constants
import random

class Wave(pygame.sprite.Sprite):
		
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
		self.frames.append('pics/wave1.gif')

	def get_image(self):
		self.frame_idx = 0
		tmp_image = pygame.image.load(self.frames[self.frame_idx]).convert()
		tmp_rect = tmp_image.get_rect()
		tmp_image = pygame.transform.scale(tmp_image , (int(tmp_rect.width * constants.WAVE_MULTIPLIER) , int(tmp_rect.height * constants.WAVE_MULTIPLIER)))
		return tmp_image

	def update(self , state , viewport , sstop):
		self.rect.x += constants.MOV_LEFT
		if state == 'l':
			if viewport == 0 and sstop == 0:
				self.rect.x += constants.MOV_RIGHT
		elif state == 'r':
			if viewport == 0 and sstop == 0:
				self.rect.x += constants.MOV_LEFT
