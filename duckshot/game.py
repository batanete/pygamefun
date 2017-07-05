import pygame
from random import randint,random
import math
import solidsprite
 
# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREEN = (0,255,0)

SPEED=10
FPS=30
 
player_width=20
player_height=20
player=None

scr_width=800
scr_height=400

points=0

clock = pygame.time.Clock()
done = False

allspriteslist=solidsprite.allspriteslist

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (scr_width,scr_height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Plate(solidsprite.SolidSprite):
	PLATE_WIDTH=25
	PLATE_HEIGHT=25
	PLATE_IMAGE_PATH='images/plate.png'
	
	current=None
	
	def __init__(self,x,y,forcex,forcey):
		super().__init__(x,y,width=Plate.PLATE_WIDTH,height=Plate.PLATE_HEIGHT,imagepath=Plate.PLATE_IMAGE_PATH,fallable=True,collidable=False)
		self.applyforce(forcex,forcey)
		Plate.current=self
		
	def update(self):
		global points
		# check if player clicked plate and delete it if it did
		ev = pygame.event.get()
		mouseisdown=False
		for event in ev:
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouseisdown=True
				break
		
		pos=pygame.mouse.get_pos()
		
		if mouseisdown and self.rect.collidepoint(pos):
			self.delete()
			Plate.current=None
			points+=1
			return
		else:
			super(Plate,self).update()
	
	def randomplate():
		"""Generates a plate with randomized initial position and velocity."""
		x=0
		y=randint(scr_height/5,scr_height/2)
		
		forcex=randint(5,8)
		forcey=randint(1,4)
		
		#forcex=0
		#forcey=0
		
		return Plate(x,y,forcex,-forcey)
	
	#creates a new plate if the last one has been destroyed.
	def updateplates():
		if Plate.current is None:
			Plate.current=Plate.randomplate()
		elif not Plate.current.isonscreen():
			Plate.current=Plate.randomplate()

# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([scr_width, scr_height])
 
# Set the title of the window
pygame.display.set_caption('Duck shot')


#sprite update function
fsprites=solidsprite.SolidSprite.updateall

def activatemusic(filename):
	pygame.mixer.music.load(filename)
	pygame.mixer.music.play()

def printpoints():
   font=pygame.font.Font(None,30)
   scoretext=font.render("Score:"+str(points), 1,(255,255,255))
   screen.blit(scoretext, (0, 0))

plate=None
BackGround=None

def initlevel():
	global plate,BackGround
	
	BackGround = Background('images/hotgirl.jpg', [0,0])
	

def main():
	global BackGround,plate
	
	initlevel()
	
	done=False
	while not done:
		
		fsprites()
		Plate.updateplates()
		
		
		# -- Draw everything
		# Clear screen
		screen.fill([0, 0, 0])
		screen.blit(BackGround.image, BackGround.rect)
		printpoints()
				
		#printpoints()
		allspriteslist.draw(screen)
 
		# Flip screen
		pygame.display.flip()
		# Pause
		clock.tick(FPS)
	
	pygame.quit()


main()


