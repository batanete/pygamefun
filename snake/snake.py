"""
 Simple snake example.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

"""

import pygame
from random import randint,choice

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY=(200,200,200)
RED = (255, 0, 0)
BLUE = (0,0,255)


GREEN = (0,255,0)

# Set the width and height of each snake segment
segment_width = 20
segment_height = 20
# Margin between each segment
segment_margin = 0

#speed
speed=14

#screen size
scr_width=14*segment_width
scr_height=11*segment_height

#this matrix allows us to tell what sections do not contain a snake segment when setting food
board_mat=[]

#game pause flag
paused=False

#initial number of segments
init_seg=1

#segments gained per food collected
seg_food=1

# Set initial speed
x_change = (segment_width + segment_margin)
y_change = 0
direction='r'


class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """
    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])

        self.image.fill(BLUE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def changecolor(self,color):
        self.image.fill(color)

class Food(pygame.sprite.Sprite):
    """ Class to represent one piece of food. """
    # -- Methods
    # Constructor function
    def __init__(self, x, y,bonus=False):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        if not bonus:
            self.image.fill(GREEN)
            self.bonus=False
        else:
            self.image.fill(WHITE)
            self.bonus=True

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([scr_width, scr_height])

# Set the title of the window
pygame.display.set_caption('Snake Example')

allspriteslist = pygame.sprite.Group()

#initialize board matrix
for i in range(int(scr_width/segment_width)):
    for j in range(int(scr_height/segment_height)):
        board_mat.append((i*segment_width,j*segment_height))


# Create an initial snake
snake_segments = []
i=init_seg
while i>0:
    x=(segment_width+segment_margin) * i
    y=0
    segment = Segment(x, y)

    #remove positions from the board matrix
    board_mat.remove((x,y))

    snake_segments.append(segment)
    allspriteslist.add(segment)
    i-=1


highscore=0
food=None
points=0
foodcounter=0

#reads high score from the text file
def readHighScore():
	global highscore

	f=open('highscore.txt','r')
	highscore=int(f.read())
	f.close()

#saves high score to the text file,if you beat it
def saveHighScore():
	global points,highscore

	if points<=highscore:
		return

	f=open('highscore.txt','w')
	highscore=f.write(str(points))
	f.close()



#create a food piece at a random location
def setfood():
	global food,foodcounter,board_mat

	#x=randint(0,scr_width/segment_width-1)*segment_width
	#y=randint(0,scr_height/segment_height-1)*segment_height

	pos=choice(board_mat)
	x=pos[0]
	y=pos[1]

	if foodcounter==5:
		food=Food(x,y,True)
		foodcounter=0
	else:
		food=Food(x,y)
		foodcounter+=1
	allspriteslist.add(food)

setfood()


clock = pygame.time.Clock()
done = False
gained_segs=0

def activatemusic(filename):
	pygame.mixer.music.load(filename)
	pygame.mixer.music.play()


def printpoints():
   font=pygame.font.Font(None,30)
   scoretext=font.render("Score:"+str(points), 1,(255,255,255))
   screen.blit(scoretext, (0, 0))

try:
	activatemusic('xutosnsou.mp3')
except:
	pass



readHighScore()

while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:

            if event.key==pygame.K_p:
                print('ola')
                if not paused:
                    paused=True
                else:
                    paused=False
                break

            if event.key == pygame.K_LEFT and direction!='r':
                direction='l'
                x_change = (segment_width + segment_margin) * -1
                y_change = 0
                break

            if event.key == pygame.K_RIGHT and direction!='l':
                direction='r'
                x_change = (segment_width + segment_margin)
                y_change = 0
                break
            if event.key == pygame.K_UP and direction!='d':
                direction='u'
                x_change = 0
                y_change = (segment_height + segment_margin) * -1
                break

            if event.key == pygame.K_DOWN and direction!='u':
                direction='d'
                x_change = 0
                y_change = (segment_height + segment_margin)
                break

    if paused:
        continue

    eaten=False


    # Figure out where new segment will be
    #remove position from board matrix
    x = (snake_segments[0].rect.x + x_change)%scr_width
    y = (snake_segments[0].rect.y + y_change)%scr_height
    segment = Segment(x, y)

    try:
        board_mat.remove((x,y))

    except:
        pass


    # Insert new segment into the list
    snake_segments.insert(0, segment)
    allspriteslist.add(segment)
    snake_segments[0].changecolor(BLUE)
    snake_segments[1].changecolor(BLUE)

    if snake_segments[0].rect.x==food.rect.x and snake_segments[0].rect.y==food.rect.y:
        if food.bonus:
            points+=5
        else:
            points+=1
        allspriteslist.remove(food)
        setfood()
        if not food.bonus:
            eaten=True
        gained_segs+=seg_food
    #bonus food doesn't grow snake
    if (not eaten):
        if gained_segs==0:
        # Get rid of last segment of the snake
        # .pop() command removes last item in list
        #add position to board matrix
            old_segment = snake_segments.pop()
            board_mat.append((old_segment.rect.x,old_segment.rect.y))
            allspriteslist.remove(old_segment)
        else:
            gained_segs-=1


    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)
    printpoints()
    allspriteslist.draw(screen)

    # Flip screen
    pygame.display.flip()

    for i in range(1,len(snake_segments)):
        if snake_segments[i].rect.x==snake_segments[0].rect.x and snake_segments[i].rect.y==snake_segments[0].rect.y:
            saveHighScore()
            print('game over')
            done=True
            quit()

    # Pause
    clock.tick(speed)

pygame.quit()
