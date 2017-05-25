## Space Adventure Game ##
## Scott Jarvis        ##
## 24/11/16            ##

#    This will require at least 2 of the below:
#	2D arrays, arrays of records or linked lists
#	a binary search, sort algorithm or other coding of similar complexity
#	Recursion
##	HTML form processing using server-side scripting
##	appropriate SQL operations

import pygame, math, random, time

# Classes

class rocket(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        baseImg = pygame.image.load("baseRocket.png")
        self.image = pygame.Surface([100,37])
        self.image.set_colorkey(black)
        self.image.blit(baseImg,(0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0  
        
    def followMouse(self, mousePos):
        self.rect.x = (mousePos[0] - 40)
        self.rect.y = (mousePos[1] - 10)
        
    #def fireLaser(self, isFiring):
        #if isFiring == True:
            #
            
            
class obstacle(pygame.sprite.Sprite):
    
    def __init__(self,name,x,y,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.name = name
        
        baseImg = (str(name) + str(size)) # loads the right size of meteor
        self.image = pygame.Surface([(24 * size),(19 * size)]) # multiplies the size of the object by the meteor size
        self.image.set_colorkey(black)
        self.image.blit(baseImg,(0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.x -= self.speed
    
    def split(self,proCount):
        for i in range(proCount):
            dista = random.randint(10, 50)
            distb = random.randint(10, 50)
            nam = ("babyMeteor" + str(i))
            makeMeteor(nam, (self.size - 1), (self.rect.x + dista), (self.rect.y + distb))
    

pygame.init()
score = 0
timeCount = 0
outScroll = 0
midScroll = 0
inScroll  = 0
screen = pygame.display.set_mode([1000,500]) 
pygame.display.set_caption("Space Survival")       
isRunning = True
clock = pygame.time.Clock()                
black    = (   0,   0,   0)                
white    = ( 255, 255, 255)                 

entities = pygame.sprite.Group()

mousePos = [0]*2
cursor = rocket()
cursor.add(entities)

# Functions and Procedures

def makeMeteor(name,size,x,y):
    meteor = obstacle(name, x, y, size)

# -------- Main Program Loop -----------
worldState = 1
scroll = 0
while isRunning == True:
    for event in pygame.event.get():        # Check for an event (mouse click, key press)
        if event.type == pygame.QUIT:       # If user clicked close window
            done = True                     # Flag that we are done so we exit this loop
    if event.type == pygame.MOUSEMOTION:
        mousePos[:] = list(event.pos)
        if worldState == 1:
            pygame.mouse.set_visible(False)
            cursor.followMouse(mousePos)
        else:
            pygame.mouse.set_visible(True)

    # Update sprites
    backgroundImg = pygame.image.load("space1.png")
    screen.fill(black)
    screen.blit(backgroundImg, [scroll,0])
    entities.draw(screen)
    pygame.display.flip()
    timeCount += 1
    scroll -= 1
    if scroll <= -600:
        scroll = 600
    clock.tick(60)                 

pygame.quit()                  

