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
        self.image = pygame.Surface([50,21])
        self.image.set_colorkey(black)
        self.image.blit(baseImg,(0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0  
        
    def followMouse(self, mousePos):
        self.rect.x = mousePos[0]
        self.rect.y = mousePos[1]       
        
    #def fireLaser(self, isFiring):
        #if isFiring == True:
            #
    


pygame.init()                               

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

# -------- Main Program Loop -----------
worldState = 0
while isRunning == True:
    for event in pygame.event.get():        # Check for an event (mouse click, key press)
        if event.type == pygame.QUIT:       # If user clicked close window
            done = True                     # Flag that we are done so we exit this loop
    if event.type == pygame.MOUSEMOTION:
        mousePos[:] = list(event.pos)
        cursor.followMouse(mousePos)


    for event in pygame.event.get():        
        if event.type == pygame.QUIT:      
            done = True                  

    # Update sprites
    
    #screen.fill(black)
    entities.draw(screen)
    pygame.display.flip()                 
    clock.tick(60)                 

pygame.quit()                  

