import pygame
import math

"""This script is meant to give you a more complete kind of Sprite object that can handle collisions and gravity."""


METER=10.0

GRAV_ACCELERATION=9.8*METER/1000

#ratio at which an object slows down when moving.the value gets multiplied by current speed before decreasing.
AIR_RESISTANCE_RATIO=0.1/1000

airresistance=True


def setgravity(grav):
	"""Sets gravity acceleration per pygame tick."""
	GRAV_ACCELERATION=grav
	
def setairresistance(ratio):
	global AIR_RESISTANCE_RATIO
	"""Sets air deacceleration per pygame tick."""
	AIR_RESISTANCE_RATIO=ratio
	
def toggleairresistance(state):
	"""turns air resistance on/off according to boolean value given."""
	airresistance=state
	

allspriteslist = pygame.sprite.Group()

class SolidSprite(pygame.sprite.Sprite):
	"""Your objects should derive from this class."""
	
	object_list=[]
	collidables_list=[]
	
	
	
	def __init__(self,x,y,fallable=False,collidable=False,imagepath=None,width=10,height=10):
		"""class constructor"""
		# Call the parent's constructor
		super().__init__()
		self.width=width
		self.height=height
		
		# Set image
		if imagepath:
			self.image = pygame.image.load(imagepath)
			self.image = pygame.transform.scale(self.image, (width,height))
			self.image.set_colorkey((0,0,0))
		#if no image is provided,we use a blue square for collidables and white for non collidables
		else:
			self.image = pygame.Surface([width, height])
			
			if collidable:
				self.image.fill((0,0,255))
			else:
				self.image.fill((255,255,255))
			
			
		# Make our top-left corner the passed-in location.
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
		self.fallable=fallable
		self.collidable=collidable
		
		#this dictionary contains info about which directions the object is blocked from
		self.blocked={'S':False,'E':False,'N':False,'W':False}
		
		self.dx=0
		self.dy=0
		
		self.tag=None
		SolidSprite.object_list.append(self)
		
		if collidable:
			SolidSprite.collidables_list.append(self)
		
		allspriteslist.add(self)
		
	
	def update(self):
		"""updates object position on each frame according to existing walls,gravity and the forces affecting him."""
		if not self.collidable and not self.fallable:
			return
		
		if not self.collidable and self.fallable:
			self.dy+=GRAV_ACCELERATION
			self.rect.x+=self.dx
			self.rect.y+=self.dy
			
			if airresistance:
				self.dy*=(1-AIR_RESISTANCE_RATIO)
				self.dx*=(1-AIR_RESISTANCE_RATIO)
			return
		
		if self.collidable and not self.fallable:
			return
		
		for direction in self.blocked.keys():
			self.blocked[direction]=False
		
		for wall in SolidSprite.collidables_list:
			if wall==self or not self.rect.colliderect(wall.rect):
				continue
			
			val=list(self.blocked.values())
			if val.count(True)>=2:
				break	
						
			if not (self.blocked['S'] or self.blocked['N']):	
				if self.rect.bottom>=wall.rect.top: # Moving down; Hit the top side of the wall
					self.rect.bottom = wall.rect.top
					self.dy=0
					self.blocked['S']=True
					continue

				elif self.rect.top<=wall.rect.bottom: # Moving up; Hit the bottom side of the wall
					self.rect.top = wall.rect.bottom
					self.dy=0
					self.blocked['N']=True
					continue
			
			if not (self.blocked['E'] or self.blocked['W']):
				if self.rect.right>=wall.rect.left: # Moving right; Hit the left side of the wall
					self.rect.right=wall.rect.left
					self.dx=0
					self.blocked['E']=True
				
				elif self.rect.left<=wall.rect.right: # Moving left; Hit the right side of the wall
					self.rect.left=wall.rect.right
					self.dx=0
					self.blocked['W']=True
				

		
		
		if not self.blocked['S'] and self.fallable:
			self.dy+=GRAV_ACCELERATION
		
		self.rect.y+=self.dy
		self.rect.x+=self.dx
		
		if airresistance:
			self.dy*=(1-AIR_RESISTANCE_RATIO)
			self.dx*=(1-AIR_RESISTANCE_RATIO)
	
	def delete(self):
		"""removes object from the game."""
		if self.collidable:
			SolidSprite.collidables_list.remove(self)
		SolidSprite.object_list.remove(self)
		allspriteslist.remove(self)
	
	def applyforce(self,x,y):
		"""changes object velocity according to the components x/y"""
		
		if y>0 and not self.blocked['S']:
			self.dy+=y
		elif y<0 and not self.blocked['N']:
			self.dy+=y
		if x>0 and not self.blocked['E']:
			self.dx+=x
		elif x<0 and not self.blocked['W']:
			self.dx+=x
	
	def isonscreen(self):
		"""returns True if object is still at least partially on screen."""
		w,h= pygame.display.Info().current_w, pygame.display.Info().current_h
		
		if self.rect.x>=w or self.rect.y>=h:
			return False
		elif self.rect.x+self.width<0 or self.rect.y+self.height<0:
			return False
		else:
			return True
	
	
	
	def updateall():
		"""updates all currently created SolidSprites."""
		for so in SolidSprite.object_list:
			so.update()
	
			
		
def createwall(x,y,w,h,impath=None,bricksize=20):
	"""Creates a new rectangular wall with the upper left corner on (x,y) and the dimensions given."""
	if w==0 or h==0:
		return
	
	#borders
	
	SolidSprite(x,y+h*bricksize,fallable=False,collidable=True,width=w*bricksize,height=bricksize)
	
	for i in range(w):
		SolidSprite(x+i*bricksize,y,fallable=False,collidable=True,width=bricksize,height=bricksize)
		SolidSprite(x+i*bricksize,y+h*bricksize,fallable=False,collidable=True,width=bricksize,height=bricksize)
	
	for i in range(1,h-1):
		SolidSprite(x,y+i*bricksize,fallable=False,collidable=True,width=bricksize,height=bricksize)
		SolidSprite(x+w*bricksize,y+i*bricksize,fallable=False,collidable=True,width=bricksize,height=bricksize)
	
	SolidSprite(x,y,fallable=False,collidable=True,width=bricksize,height=h*bricksize)
	SolidSprite(x+w*bricksize,y,fallable=False,collidable=True,width=bricksize,height=h*bricksize)
		
	#inner bricks	
	SolidSprite(x+bricksize,y+bricksize,imagepath=impath,fallable=False,collidable=False,width=(w-1)*bricksize,height=(h-1)*bricksize)
	
	
"""
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([800,600])
 
# Set the title of the window
pygame.display.set_caption('gravity experiment')
 

def main():

	player=SolidSprite(-5,0,fallable=True,collidable=True)
	
	player.applyforce(5,-1)
	
	createwall(0,400,h=10,w=800)
	createwall(400,0,h=800,w=10)
	
	done=False
	while not done:
		
		SolidSprite.updateall()
		
		# -- Draw everything
		# Clear screen
		screen.fill([0,0,0])
		
		#player.applyforce(0.1,0.1)
		allspriteslist.draw(screen)
		
		
		# Flip screen
		pygame.display.flip()
		# Pause
		pygame.time.Clock().tick(30)
	pygame.quit()

main()
"""
