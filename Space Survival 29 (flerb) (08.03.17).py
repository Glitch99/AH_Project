# Meteor Rush          ##
# Made by Scott Jarvis ##
# 24/11/16 to __/__/17 ##

import pygame, math, random, time, csv, re


# Classes
class displayCard(pygame.sprite.Sprite):                                # This class is just for the title & game over cards that display at the start and end
    
    def __init__(self,make):          
        super(displayCard, self).__init__()
        if make == "titleCard":
            self.image =  pygame.image.load("screencards/itleScreen.png") 
            self.image.set_colorkey(white)
        elif make == "endCard":
            self.image =  pygame.image.load("screencards/gameOver.png")
            self.image.set_colorkey(white)                              # Different colourkey allows for transparency in the text
        elif make == "scoreCard":
            self.image =  pygame.image.load("screencards/scoreName.png")
            self.image.set_colorkey(black)     
       
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

class button(pygame.sprite.Sprite):
    
    def __init__(self,kind,x,y):
        pygame.sprite.Sprite.__init__(self)
        baseImg = pygame.image.load("entities/budden.png")
        self.image = pygame.Surface([90,90])
        self.image.blit(baseImg,(0,0))
           
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y  
        
    def getClicked(kind):
        if self.kind == 0:
            worldState = 1
        elif self.kind == 1:
            worldState = 3
        elif self.kind == 2:
            worldState = 4
        elif self.kind == 3:
            isRunning = False
        
        return worldState, isRunning
            
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
            self.kill                                                               # kills the object if the frame in use excedes the number of frames in the index


 
    
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
blue     = (   0,   0,   0)

font = pygame.font.Font(None, 36)

## GROUP CREATION ##

entities = pygame.sprite.Group()
cursors  = pygame.sprite.Group()
boomboom = pygame.sprite.Group()
cards    = pygame.sprite.Group()
buttons  = pygame.sprite.Group()
slices   = pygame.sprite.Group()

## VARIABLE SETUP ##

mousePos = [0]*2

space = pygame.image.load("space\ibg.png")   
backMult = [0]
score = 1
isDead = False
doomCount = 0

realTime = 0

baseMult = 1
timeDiff = 100
boostFuel = 1000

names = []
scores = []
megaList = []*2

multIsSaved = 0
timeSurvived = 0
isReversing = False
metMult = 5
metCount = 0
isBoosting = False
ticker = 0
rowRange = 0


timeTillNextObstacle = 300
worldState = 0
gameOver = False


## MISC ##
titlecard = displayCard("titleCard")
title = pygame.sprite.Group(titlecard)

endcard = displayCard("endCard")
end = pygame.sprite.Group(endcard)

scorecard = displayCard("scoreCard")
nameScreen = pygame.sprite.Group(scorecard)

startMessage = font.render("Click Anywhere to Start" ,1,white)


    

# Functions and Procedures

def takeName(nameChosen):
    if nameChosen != True:
        playerName = input("Please Enter A Name:   ")         ##input("Please Enter Your Name: ")   
        if not re.match("^[A-Z]*$", playerName):
            print("Error! Only capital letters are allowed!")
            playerName = takeName(False)
        elif len(playerName) > 4:
            print("Error! Only four characters are allowed!")
            playerName = takeName(False)
        else:
            nameChosen = True
        return playerName
        
        
def load_image(name):                           # For animated image loading
    image = pygame.image.load(name)
    return image

def makeMeteor(x,y,metCount):                   # Creates a meteor
    metCount += 1
    name = "entities\meteor" + str(metCount)
    meteor = obstacle(name, x, y)
    meteor.add(entities)
   
def createSlice(count):
    if count != 16:
        sliced = spaceSlice(0, 0, "space\background" + str(count) + ".png")
        sliced.add(slices)
        createSlice(count + 1)

def bubbleSort(inputData,ranging):
    swapcount = 0
    passes = 0
    comparisons = 0
    sorted = False
    
    while sorted == False:
        outerloop = (ranging - 1)
        swaps = 0
        
        for i in range (outerloop):
            comparisons = comparisons + 1
            if inputData[i][1] < inputData[i + 1][1]:
                temp = inputData[i]
                inputData[i] = inputData[i + 1]
                inputData[i + 1] = temp
                swaps = swaps + 1
                swapcount = swapcount + 1
        if swaps == 0:
            sorted = True
        outerloop = outerloop - 1
        passes = passes + 1
        
    outputData = inputData
    return outputData

def hyperSpace(spaceX,baseMult):
    
    screen.fill(black)     
    screen.blit(space, [spaceX[0],0])

    spaceX[0] -= baseMult * 1.5                                # Increases the speed at which the backgrounds scroll


    if spaceX[0] <= -1000 or spaceX[0] >= 1000:                               # Resets the backgrounds should they go past a certain point, creating a
        spaceX[0] = 0                                                         # psuedo-infinite background
        
        
    return backMult
        
def playMusic(state):
    pygame.mixer.music.load("music\mus" + str(state) +".ogg")        
    pygame.mixer.music.play(-1,0.0)
    
# -------- Main Program Loop -----------


while isRunning == True:
    
    if pygame.mixer.music.get_busy() == False:
        playMusic(worldState)
    
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
            
    if worldState == 0:
        startGameButton = button(0, 0, 0)
        highScoreButton = button(1, 200, 200)
        helpMePlsButton = button(2, 50, 200)
        leaveGameButton = button(3, 100, 200)

        startGameButton.add(buttons)
        highScoreButton.add(buttons)
        helpMePlsButton.add(buttons)
        leaveGameButton.add(buttons)
        
    while worldState == 0:
    
        hyperSpace(backMult,baseMult) 
        
        
        realTime     = 0
        baseMult     = 1
        timeDiff     = 100
        boostFuel    = 1000
        score        = 0

        multIsSaved  = 0
        timeSurvived = 0
        isReversing  = False 
        isBoosting   = False
        isDead       = False
        metMult      = 5
        metCount     = 0

        ticker = 0


        for toKill in (entities.sprites()):            
            pygame.sprite.Sprite.kill(toKill)


        
        title.draw(screen)
        #buttons.draw(screen)
        screen.blit(startMessage, (350,350))
        
            
        pygame.display.flip()  
        clock.tick(60) 

        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                worldState = 1                                                  #ends title screen
        
                pygame.mixer.music.stop()
        
                cursor = rocket()
                cursor.add(cursors)  
                
                tutPassed = False
                metNumb = 0

    if worldState == 1:
        
        pygame.mixer.music.set_volume(0.5)
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
        

        curFuel      = font.render("Boost Fuel: " + str((round(boostFuel / 10,0))) + "%",1,white)        # displays the current score, fuel, and time survived
        scoreDisplay = font.render("Distance Travelled: " + str(score) + "m", 1, white)
        timeDisplay  = font.render("Time Survived: " + str(timeSurvived), 1, white)       
           
    
        # Make Obstacles #     

        if pygame.time.get_ticks() > timeTillNextObstacle and tutPassed == True:                          # Creates a new meteor if enough time has passed
            yCoord = random.randint(-50,550)                                        # Sets a random y-coordinate for the meteor
            makeMeteor(1100,yCoord,metCount)
            timeTillNextObstacle += (random.randint(500,2000) / baseMult)           # Increases the value of timeTillNextObstacle by a random integer
        elif tutPassed == False and pygame.time.get_ticks() > timeTillNextObstacle:
            makeMeteor(1100,400,metCount)
            timeTillNextObstacle += 300
            metNumb += 1
            if metNumb == 3:
                tutPassed = True
            


    # Update sprites
    
    hyperSpace(backMult,baseMult)
    
    if worldState == 1:                             # Updates the items on screen during gameplay
        
        screen.blit(curFuel,      (10 ,450))
        screen.blit(scoreDisplay, (700,450))
       


        boomboom.update()
        boomboom.draw(screen)   
        entities.draw(screen)
        cursors.draw(screen)


        if realTime > timeDiff:                     # Exponentially increases the speed of the game as it goes on
            baseMult *= 1.001
            if boostFuel < 1000:
                boostFuel *= 1.001
            
        
        realTime += 1   # Keeps track of the time the player has survived for
            
            
        for mp in (entities.sprites()):    # Moves the meteorite particles (mp) at slightly faster than the base multiplier
            mp.moveIt(baseMult * 1.6)
            if mp.rect.x < -100:           # removes a meteor if it goes too far off screen, removing any slowdown
                pygame.sprite.Sprite.kill(mp) 
                
        pygame.sprite.groupcollide(cursors, entities, True, False)   # If the cursor and a meteor collide, the cursor will be killed
        
        if len(cursors.sprites()) == 0 and isDead == False:
            isDead = True
            boom = explosion(cursor.rect.x - 10, cursor.rect.y - 40, "death")        # Creates an explosion at the location where the cursor was
            boom.add(boomboom)
            doomCount = realTime + 50

            
      
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
          
    
    if realTime == doomCount:
        pygame.mixer.music.stop()
        worldState = 2
        doomCount = 0
  
    if worldState == 2:
    
        end.draw(screen)
        finalScore = (score + realTime)
        endMessage   = font.render("Your final score was " + str(finalScore) + " points", 1, white)     
        screen.blit(endMessage, (350,350))


        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:                
                pygame.mixer.music.stop()
                worldState = 3
                
        pygame.display.flip()  
        clock.tick(60)   
        
    while worldState == 3:
        
        hyperSpace(backMult,baseMult)        
        
        nameScreen.draw(screen)
                                                                                 # Input Name
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN: # Change to ENTER pressed
                
                playerName = takeName(False)
                
                with open("scoreList.csv", "r") as sl1:
                    reader = csv.reader(sl1)
                
                    for row in reader:
                        names.append(row[0])                                                
                        scores.append(int(row[1]))
                    
                
                names.append(playerName)
                scores.append(finalScore)
                
                for count in range(len(scores)):
                    print(names[count], "+",scores[count])
                    megaList.append([names[count],scores[count]])
                
                
## SORT SCORES ##
                
                finalCSV = bubbleSort(megaList, len(scores))
                with open("scoreList.csv","w", newline="") as sl:
                    writer = csv.writer(sl)
                    for row in range(len(scores)):
                        writer.writerow(finalCSV[row])
               
                
    
                pygame.mixer.music.stop()
                worldState = 0  
                    
                    
        pygame.display.flip()        
        clock.tick(60)                      
                

    
            
    pygame.display.flip()        
    clock.tick(60)  


pygame.quit()                  