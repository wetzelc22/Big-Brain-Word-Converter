import pygame
#import converter.py



white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128)
black = (0, 0, 0)

X = 700
Y = 700

class user_interface:
	def __init__(self):


		pygame.init()
		self.screen = pygame.display.set_mode((X, Y))
		self.background = pygame.Surface(self.screen.get_size()).convert()

		self.font = pygame.font.Font("minimal5x7.TTF", 50)
		self.text = self.font.render('Enter your file to see it at 200 IQ ', True, black, white)
		self.textRect = self.text.get_rect()
		self.textRect.center = (X // 2, Y // 2)

	def mainLoop(self):

		self.done = False
		while not self.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
						self.done = True
			self.screen.fill(white)

			self.screen.blit(self.text, self.textRect)
			pygame.display.update()

			
	pygame.quit

def main():
	userInterface = user_interface()
	userInterface.mainLoop()

main()