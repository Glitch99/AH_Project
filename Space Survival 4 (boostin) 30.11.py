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
    
    def __init__(self,name,x,y,speed):
        
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.speed = speed
        
        baseImg = pygame.image.load(name + ".png") # loads the right size of meteor
        self.image = pygame.Surface([(24),(19)]) # multiplies the size of the object by the meteor size
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

realTime = 0
outScroll = 0
midScroll = 0
inScroll  = 0
cenScroll = 0

outImg = pygame.image.load("space1.png")
midImg = pygame.image.load("space2.png")
inImg = pygame.image.load("space3.png")
cenImg = pygame.image.load("space4.png")

screen = pygame.display.set_mode([1000,500]) 
pygame.display.set_caption("Space Survival")       
isRunning = True
clock = pygame.time.Clock()                
black    = (   0,   0,   0)                
white    = ( 255, 255, 255)    

font = pygame.font.Font(None, 36)

entities = pygame.sprite.Group()

mousePos = [0]*2
cursor = rocket()
cursor.add(entities)

baseMult = 1
timeDiff = 100
boostFuel = 1000
multIsSaved = 0
timeSurvived = 0
isReversing = False
# Functions and Procedures

def makeMeteor(x,y,speed):
    name = "meteor"
    meteor = obstacle(name, x, y, speed)

    
# -------- Main Program Loop -----------
worldState = 1
timeTillNextObstacle = 0
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
            
    if worldState == 1:
        if isReversing == False:
            score += .5 * baseMult
            score = int(round(score, 1))
        else:
            score += .25 * baseMult
            score = int(round(score, 1))            
        if pygame.mouse.get_pressed()[0] and boostFuel > 0:
            if multIsSaved == 0:
                saveMult = baseMult
                multIsSaved = 1
            
            baseMult += 0.2
            boostFuel -= 4
            
        elif multIsSaved == 1:
            if baseMult > saveMult + 2:
                baseMult -= .5
                isReversing = True
            else:
                multIsSaved == 0
                isReversing = False
        
        curFuel =      font.render("Boost Fuel: " + str((boostFuel / 10)) + "%",1,white)
        scoreDisplay = font.render("Distance Travelled: " + str(score), 1, white)
        timeDisplay =  font.render("Time Survived: " + str(timeSurvived), 1, white)       
           
    
    # Make Obstacles #     
        if worldState == 1:
            if pygame.time.get_ticks() > timeTillNextObstacle:
                timeTillNextObstacle += random.randint(0,5000)
                
                yCoord = random.randint(-50,550)
                makeMeteor(500,yCoord,1)
            

    # Update sprites
    
    screen.fill(black)

    screen.blit(outImg, [outScroll,0])
    screen.blit(midImg, [midScroll,50]) 
    screen.blit(inImg, [inScroll,107]) 
    screen.blit(cenImg, [cenScroll,160])
    
    screen.blit(curFuel,      (10 ,450))
    screen.blit(scoreDisplay, (700,450))
    screen.blit(timeDisplay,  (751,50 ))
   
    entities.draw(screen)
    pygame.display.flip()
    

    
    if realTime > timeDiff:
        baseMult *= 1.001


    
    
    realTime += 1
    outScroll -= baseMult * 1.6
    midScroll -= baseMult * 1.4
    inScroll  -= baseMult * 1.2
    cenScroll -= baseMult * 1
    
    
   
    
    if outScroll <= -1500 or outScroll >= 1000:
        outScroll = 0
    if midScroll <= -1750 or midScroll >= 1000:
        midScroll = 0  
    if inScroll <= -1750 or inScroll >= 1000:
        inScroll = 0  
    if cenScroll <= -1750 or cenScroll >= 1000:
        cenScroll = 0  
        
    #print(str(outScroll) + "," + str(midScroll) + "," + str(inScroll) + "," + str(cenScroll)
    timeSurvived = int(round(realTime / 10,0))
    print(str(timeSurvived))
    clock.tick(120)                 

pygame.quit()                  

