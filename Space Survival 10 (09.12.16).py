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
class displayCard(pygame.sprite.Sprite):
    
    def __init__(self,make):          
        super(displayCard, self).__init__()
        if make == "titleCard":
            self.image =  pygame.image.load("screencards/itleCard1.png") 
            self.image.set_colorkey(black)
        if make == "endCard":
            self.image =  pygame.image.load("screencards/gameOver.png")
            self.image.set_colorkey(white)
            
       
        self.rect = pygame.Rect(0, 0, 1000, 500)

            
class rocket(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        baseImg = pygame.image.load("entities/baseRocket.png")
        self.image = pygame.Surface([100,37])
        self.image.set_colorkey(black)
        self.image.blit(baseImg,(0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0  
        
    def moveIt(self, mousePos):
        self.rect.x = (mousePos[0] - 40)
        self.rect.y = (mousePos[1] - 10)
        
    #def fireLaser(self, isFiring):
        #if isFiring == True:
            #
            
class explosion(pygame.sprite.Sprite):
    
    def __init__(self,x,y):          
        super(explosion, self).__init__()
        self.images = []
        for count in range(13):
            self.images.append(load_image("explode\pic" + str(count) + ".gif"))
            count += 1
        # assuming both images are 64x64 pixels
    
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x, y, 200, 200)


        
    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        self.index += 1
        ded = False
        if self.index >= len(self.images):
            ded = True
        if ded != True:
            self.image = self.images[self.index]
        else:
            self.kill

    
class obstacle(pygame.sprite.Sprite):
    
    def __init__(self,name,x,y):
        
        pygame.sprite.Sprite.__init__(self)

        baseImg = pygame.image.load("entities\meteor.png")
    
        
        self.image = pygame.Surface([150,105]) 
    
        self.image.set_colorkey(white)
        
        self.image.blit(baseImg,(0,0))
    
        self.rect = self.image.get_rect() #m8
        self.rect.x = x
        self.rect.y = y  
        
        
    def moveIt(self, speed):
        self.rect.x -= speed
    
    def split(self,proCount):
        for i in range(proCount):
            dista = random.randint(10, 50)
            distb = random.randint(10, 50)
            nam = ("babyMeteor" + str(i))
            makeMeteor(nam, (self.size - 1), (self.rect.x + dista), (self.rect.y + distb))
    

pygame.init()

score = 1
isDead = False

realTime = 0
outScroll = 0
midScroll = 0
inScroll  = 0
cenScroll = 0

outImg    = pygame.image.load("background\space1.png")
midImg    = pygame.image.load("background\space2.png")
inImg     = pygame.image.load("background\space3.png")
cenImg    = pygame.image.load("background\space4.png")


screen = pygame.display.set_mode([1000,500]) 
pygame.display.set_caption("")       
isRunning = True
clock = pygame.time.Clock()                
black    = (   0,   0,   0)                
white    = ( 255, 255, 255)    

font = pygame.font.Font(None, 36)

entities = pygame.sprite.Group()
cursors = pygame.sprite.Group()
boomboom = pygame.sprite.Group()
cards = pygame.sprite.Group()

titlecard = displayCard("titleCard")
title = pygame.sprite.Group(titlecard)
endcard = displayCard("endCard")
end = pygame.sprite.Group(endcard)



mousePos = [0]*2
cursor = rocket()
cursor.add(cursors)

baseMult = 1
timeDiff = 100
boostFuel = 1000
multIsSaved = 0
timeSurvived = 0
isReversing = False
metMult = 5
metCount = 0
isBoosting = False
ticker = 0
showMess = False

startMessage = font.render("Press any key to Start" ,1,white)


# Functions and Procedures

def load_image(name):
    image = pygame.image.load(name)
    return image

def makeMeteor(x,y,metCount):
    metCount += 1
    name = "entities\meteor" + str(metCount)
    meteor = obstacle(name, x, y)
    meteor.add(entities)
    
# -------- Main Program Loop -----------

worldState = 0
gameOver = False
timeTillNextObstacle = 10

while isRunning == True:
    for event in pygame.event.get():        # Check for an event (mouse click, key press)
        if event.type == pygame.QUIT:       # If user clicked close window
            isRunning = False                     # Flag that we are done so we exit this loop
            
    if event.type == pygame.MOUSEMOTION:
        mousePos[:] = list(event.pos)
        if worldState == 1 or worldState == 2:
            pygame.mouse.set_visible(False)
            cursor.moveIt(mousePos)
        else:
            pygame.mouse.set_visible(True)
            
    while worldState == 0:
             
        title.draw(screen)
        
        screen.blit(startMessage, (350,350))
            
        pygame.display.flip()  
        clock.tick(60) 

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                worldState = 1    

    if worldState == 1:
            
        if pygame.mouse.get_pressed()[0] and boostFuel > 0:
            if multIsSaved == 0:
                saveMult = baseMult
                multIsSaved = 1
            
            baseMult += 0.2
            boostFuel -= 4
            isBoosting = True
            
        elif multIsSaved == 1:
            if baseMult > saveMult + 2:
                baseMult -= .5
                isReversing = True
                isBoosting = False
            else:
                multIsSaved == 0
                isReversing = False
        
           
        
        curFuel      = font.render("Boost Fuel: " + str((boostFuel / 10)) + "%",1,white)
        scoreDisplay = font.render("Distance Travelled: " + str(score) + "m", 1, white)
        timeDisplay  = font.render("Time Survived: " + str(timeSurvived), 1, white)       
           
    
    # Make Obstacles #     

        if pygame.time.get_ticks() > timeTillNextObstacle:
            yCoord = random.randint(-50,550)
            makeMeteor(1100,yCoord,metCount)
            timeTillNextObstacle += random.randint(250,1500)


    # Update sprites
    
    screen.fill(black)

    
    screen.blit(outImg, [outScroll,0])
    screen.blit(midImg, [midScroll,50]) 
    screen.blit(inImg, [inScroll,107]) 
    screen.blit(cenImg, [cenScroll,160])
    
    if worldState == 1: 
        screen.blit(curFuel,      (10 ,450))
        screen.blit(scoreDisplay, (700,450))
        screen.blit(timeDisplay,  (751,50 ))
        
        

        boomboom.update()
       
        entities.draw(screen)
        cursors.draw(screen)
        boomboom.draw(screen)  

        if realTime > timeDiff:
            baseMult *= 1.001
        
      
    
    outScroll -= baseMult * 1.3
    midScroll -= baseMult * 1.2
    inScroll  -= baseMult * 1.1
    cenScroll -= baseMult * 1
    
    
   
    
    if outScroll <= -1000 or outScroll >= 1000:
        outScroll = 0
    if midScroll <= -1000 or midScroll >= 1000:
        midScroll = 0  
    if inScroll <= -1000 or inScroll >= 1000:
        inScroll = 0  
    if cenScroll <= -1000 or cenScroll >= 1000:
        cenScroll = 0
    
    if worldState == 1:
    
        realTime += 1
            
        for mep in (entities.sprites()):
            mep.moveIt(baseMult * 1.7)
            if mep.rect.x < -100:
                pygame.sprite.Sprite.kill(mep) 
                
        pygame.sprite.groupcollide(cursors, entities, True, False)
        
        if len(cursors.sprites()) == 0 and isDead == False:
            isDead = True
            boom = explosion(cursor.rect.x, cursor.rect.y)
            boom.add(boomboom)
            worldState = 2
      
        if isDead == False:   
    
            timeSurvived = int(round(realTime / 10,0))
            if isReversing == False:
                score += baseMult * 0.9
                score = int(round(score, 1))
            else:
                score += .25 * baseMult
                score = int(round(score, 1))
        else:
            for toKill in (entities.sprites()):
                if toKill.rect.x > 1000:
                    pygame.sprite.Sprite.kill(toKill)
         

        
    if worldState == 2:
    
        end.draw(screen)
    
        endMessage = font.render("You Lose: Your final score was " + str(score) + "." ,1,white)
            
        screen.blit(endMessage, (350,350))
        
        
        pygame.display.flip()  
        clock.tick(60) 

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                worldState = 0

            
    pygame.display.flip()        
    clock.tick(60)                 

pygame.quit()                  

