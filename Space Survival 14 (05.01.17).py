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
class displayCard(pygame.sprite.Sprite):                                # This class is just for the title & game over cards that display at the start and end
    
    def __init__(self,make):          
        super(displayCard, self).__init__()
        if make == "titleCard":
            self.image =  pygame.image.load("screencards/itleCard1.png") 
            self.image.set_colorkey(black)
        if make == "endCard":
            self.image =  pygame.image.load("screencards/gameOver.png")
            self.image.set_colorkey(white)                              # Different colourkey allows for transparency in the text
            
       
        self.rect = pygame.Rect(0, 0, 1000, 500)

            
class rocket(pygame.sprite.Sprite):                                     #This class is the "rocket" controlled by the cursor
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        baseImg = pygame.image.load("entities/rocketBody.png")
        self.image = pygame.Surface([65,25])
        self.image.set_colorkey(black)
        self.image.blit(baseImg,(0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0  
        
    def moveIt(self, mousePos):                                        #constantly sets the current position of the rocket to just behind the cursor, as to avoid going off window
        self.rect.x = (mousePos[0] - 40)
        self.rect.y = (mousePos[1] - 10)
        
    #def fireLaser(self, isFiring):                                   ## Will eventually fire lasers ##
        #if isFiring == True:
            #
            
class explosion(pygame.sprite.Sprite):
    
    def __init__(self,x,y,why):          
        super(explosion, self).__init__()
        self.images = []

        for count in range(13): 
            self.images.append(load_image("explode\pic" + str(count) + ".gif"))     # adds all of the frames of the explosion in the folder to the array
            count += 1

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x - 10, y - 40, 200, 200)



    def update(self):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        self.index += 1
        ded = False
        if self.index >= len(self.images):
            ded = True
        if ded != True:
            self.image = self.images[self.index]                                    # sets the image to display for the object to the current image in the index
        else:
            boomdone = True
            self.kill                                                               # kills the object if the frame in use excedes the number of frames in the index
            return boomdone


    
class obstacle(pygame.sprite.Sprite):
    
    def __init__(self,name,x,y):
        
        pygame.sprite.Sprite.__init__(self)

        baseImg = pygame.image.load("entities\meteorBase.png")
    
        
        self.image = pygame.Surface([90,90]) 
    
        self.image.set_colorkey(white)
        self.image.blit(baseImg,(0,0))
    
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y  
        
        
    def moveIt(self, speed):                                    #constantly moves the meteor to the left at the rate of "speed"
        self.rect.x -= speed
    
    def split(self,proCount):                                   #if shot, the meteor creates three smaller meteorites to avoid
        for i in range(proCount):
            dista = random.randint(10, 50)
            distb = random.randint(10, 50)
            nam = ("babyMeteor" + str(i))
            makeMeteor(nam, (self.size - 1), (self.rect.x + dista), (self.rect.y + distb))
    
## PYGAME INITIALISATION ##
            
pygame.init()

screen = pygame.display.set_mode([1000,500]) 
pygame.display.set_caption("")       
isRunning = True
clock = pygame.time.Clock()                
black    = (   0,   0,   0)                
white    = ( 255, 255, 255)    

font = pygame.font.Font(None, 36)

## GROUP CREATION ##

entities = pygame.sprite.Group()
cursors = pygame.sprite.Group()
boomboom = pygame.sprite.Group()
cards = pygame.sprite.Group()

## VARIABLE SETUP ##
mousePos = [0]*2

score = 1
isDead = False
boomdone = False

realTime = 0
outScroll = 0
midScroll = 0
inScroll  = 0
cenScroll = 0

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

worldState = 0
gameOver = False
timeTillNextObstacle = 300

## MISC ##
outImg    = pygame.image.load("background\space1.png")                                  # creates four backgrounds, each with a different image
midImg    = pygame.image.load("background\space2.png")
inImg     = pygame.image.load("background\space3.png")
cenImg    = pygame.image.load("background\space4.png")

titlecard = displayCard("titleCard")
title = pygame.sprite.Group(titlecard)
endcard = displayCard("endCard")
end = pygame.sprite.Group(endcard)

cursor = rocket()
cursor.add(cursors)

startMessage = font.render("Press any key to Start" ,1,white)

    

# Functions and Procedures

def load_image(name):                           # For animated image loading
    image = pygame.image.load(name)
    return image

def makeMeteor(x,y,metCount):                   # Creates a meteor
    metCount += 1
    name = "entities\meteor" + str(metCount)
    meteor = obstacle(name, x, y)
    meteor.add(entities)
    
# -------- Main Program Loop -----------

while isRunning == True:
    
    for event in pygame.event.get():        # Check for an event 
        if event.type == pygame.QUIT:       # If user clicks close window
            isRunning = False                     
            
    if event.type == pygame.MOUSEMOTION:
        mousePos[:] = list(event.pos)       # Keeps track of the cursor position when it moves
        
        if worldState == 1 or worldState == 2: 
            pygame.mouse.set_visible(False) # Makes the mouse invisible and moves the rocket to the cursor during game over & gameplay states
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
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                worldState = 1                                                          #ends title screen

    if worldState == 1:
            
        if pygame.mouse.get_pressed()[0] and boostFuel > 0:
            if multIsSaved == 0:
                saveMult = baseMult                 #saves the original, pre-boost speed when boosting
                multIsSaved = 1
            
            baseMult += 0.2
            boostFuel -= 4
            isBoosting = True
            
        elif multIsSaved == 1:
            if baseMult > saveMult + 2:                     # lowers baseMult until the speed meets the saved copy
                baseMult -= .5
                isReversing = True
                isBoosting = False
            else:
                multIsSaved == 0
                isReversing = False
        
           
        
        curFuel      = font.render("Boost Fuel: " + str((boostFuel / 10)) + "%",1,white)        # displays the current score, fuel, and time survived
        scoreDisplay = font.render("Distance Travelled: " + str(score) + "m", 1, white)
        timeDisplay  = font.render("Time Survived: " + str(timeSurvived), 1, white)       
           
    
        # Make Obstacles #     

        if pygame.time.get_ticks() > timeTillNextObstacle:                          # Creates a new meteor if enough time has passed
            yCoord = random.randint(-50,550)                                        # Sets a random y-coordinate for the meteor
            makeMeteor(1100,yCoord,metCount)
            timeTillNextObstacle += (random.randint(500,2000) / baseMult)           # Increases the value of timeTillNextObstacle by a random integer



    # Update sprites
    
    screen.fill(black)

    
    screen.blit(outImg, [outScroll,0])                          # Updates the four backgrounds at different locations to create an illusion of movement
    screen.blit(midImg, [midScroll,50]) 
    screen.blit(inImg, [inScroll,107]) 
    screen.blit(cenImg, [cenScroll,160])
    
    if worldState == 1:                             # Updates the items on screen during gameplay
        
        screen.blit(curFuel,      (10 ,450))
        screen.blit(scoreDisplay, (700,450))
        screen.blit(timeDisplay,  (751,50 ))
        
        

        boomboom.update()
        boomboom.draw(screen)   
        entities.draw(screen)
        cursors.draw(screen)


        if realTime > timeDiff:                     # Exponentially increases the speed of the game as it goes on
            baseMult *= 1.001
        
      
    
    outScroll -= baseMult * 1.6         # Increases the speed at which the backgrounds scroll
    midScroll -= baseMult * 1.4
    inScroll  -= baseMult * 1.2
    cenScroll -= baseMult * 1
    
    
   
    
    if outScroll <= -1000 or outScroll >= 1000:                                         # Resets the backgrounds should they go past a certain point, creating a
        outScroll = 0                                                                   # psuedo-infinite background
    if midScroll <= -1000 or midScroll >= 1000:
        midScroll = 0  
    if inScroll <= -1000 or inScroll >= 1000:
        inScroll = 0  
    if cenScroll <= -1000 or cenScroll >= 1000:
        cenScroll = 0
    
    if worldState == 1:
    
        realTime += 1   # Keeps track of the time the player has survived for
            
        for mp in (entities.sprites()):    # Moves the meteorite particles (mp) at slightly faster than the base multiplier
            mp.moveIt(baseMult * 1.7)
            if mp.rect.x < -100:           # removes a meteor if it goes too far off screen, removing any unnessecary slowdown
                pygame.sprite.Sprite.kill(mp) 
                
        pygame.sprite.groupcollide(cursors, entities, True, False)   # If the cursor and a meteor collide, the cursor will be killed
        
        if len(cursors.sprites()) == 0 and isDead == False:
            isDead = True
            boom = explosion(cursor.rect.x - 10, cursor.rect.y - 40, "death")        # Creates an explosion at the location where the cursor was
            boom.add(boomboom)
            #worldState = 2
            
      
        if isDead == False:   
    
            timeSurvived = int(round(realTime / 10,0))
            
            if isReversing == False:
                score += baseMult * 0.9
                score = int(round(score, 1))
            else:
                score += .25 * baseMult             # Constantly adds to the score, unless the player is reversing or dead
                score = int(round(score, 1))
        else:
            for toKill in (entities.sprites()):             # Kills all meteors offscreen if the player is dead
                if toKill.rect.x > 1000:
                    pygame.sprite.Sprite.kill(toKill)
          
    
    if boomdone == True:
        worldState = 2
         

        
    if worldState == 2:
    
        end.draw(screen)
            
        #screen.blit(endMessage, (350,350))
            
        

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                worldState = 0
                
        pygame.display.flip()  
        clock.tick(60)   

            
    pygame.display.flip()        
    clock.tick(60)                 

pygame.quit()                  

