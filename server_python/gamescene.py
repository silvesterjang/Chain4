import pygame

class Gamescene(object):
	def __init__(self, world, scale=30):
		pygame.init()
		self.scale = scale
		self.world = world
		self.row = world.row
		self.col = world.col
		self.screen = pygame.display.set_mode((self.row * scale, self.col * scale))
		self.colors = [(0,0,0),(0xff,0,0),(0,0,0xff),(0xff,0xff,0xff),(0x20,0x20,0x20)]
		
		background = pygame.Surface(self.screen.get_size())
		background = background.convert()
		background.fill(self.colors[0])

		for i in xrange(1,self.row):
			pygame.draw.line(background, self.colors[4], (i*scale,0), (i*scale,self.col*scale))

		for j in xrange(1,self.col):
			pygame.draw.line(background, self.colors[4], (0,j*scale), (self.row*scale, j*scale))

		self.screen.blit(background, (0,0))
		self.set_caption("Chain 4")
		pygame.display.flip()

	def set_caption(self, text):
		pygame.display.set_caption(text)
	
	def update(self):
		"""
		for y in xrange(self.col):
			for x in xrange(self.row):
				player = self.colors[self.world.map[y][x]]
				pygame.draw.rect(self.screen, player, (x*self.scale+1,y*self.scale+1,self.scale-1,self.scale-1))
		pygame.display.flip()
		"""
		for row in xrange(self.row):
			for col in xrange(self.col):
				player = self.colors[self.world.map[row][col]]
				pygame.draw.rect(self.screen,player,(row*self.scale+4,(self.col-col-1)*self.scale+4 ,self.scale-8,self.scale-8))
		pygame.display.flip()
		pygame.event.pump()
