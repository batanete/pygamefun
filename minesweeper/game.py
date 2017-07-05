import pygame
from random import randint


n_mines=99

#square width,in pixels
square_width=20

#game screen dimensions,in squares
scr_dims=(30,20)

#dimension of mine field,in squares
dims=(30,16)

allspriteslist = pygame.sprite.Group()


class Square(pygame.sprite.Sprite):
    
    squares=[]
    
    def __init__(self, location, mine=False):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.Surface([square_width, square_width])
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        
        #number showing for user.if==-1 it is not visible yet.
        self.number=-1
        
        Square.squares.append(self)
        allspriteslist.add(self)

#generate mine tiles randomly
def gen_mines():
    res=[]
    
    tiles=[]
    for i in range(dims[0]):
        for j in range(dims[1]):
            tiles.append((dims[0],dims[1]))
            
    for i in range(n_mines):
        ind=randint(0,len(tiles)-1)
        
        res.append(tiles.pop(ind))
    
    return res

#draws board on screen at the beginning
def init():
    
    mines=gen_mines()
    
    for i in range(dims[0]):
        for j in range(4,4+dims[1]):
            if (i,j) in mines:
                Square((i*square_width,j*square_width),mine=True)
            else:
                Square((i*square_width,j*square_width),mine=False)
    
    
    
    

def main():
    global points,done,player
    # Call this function so the Pygame library can initialize itself
    pygame.init()
    
    #clear objects from previous game
    allspriteslist.empty()
    minesfound=0
    
    screen = pygame.display.set_mode([scr_dims[0]*square_width, scr_dims[1]*square_width])
    
    # Set the title of the window
    pygame.display.set_caption('Mines Bata')
    
    init()
    done=False
    while not done:
        # -- Draw everything
        # Clear screen
        screen.fill([0, 0, 0])
        
        allspriteslist.draw(screen)
        
        # Flip screen
        pygame.display.flip()
        # Pause
        pygame.time.Clock().tick(30)

if __name__=='__main__':
    main()
