print("Amanda Clevenger")
print("11/01/2024")
print("Slide and Catch game part 1")

import pygame, simpleGE, random

class Worm(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Worm.png")
        self.setSize(30, 30)
        self.minSpeed = 3
        self.maxSpeed = 8
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()


class Fish(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Fish.png")
        self.setSize(90, 110)
        self.position = (320, 400)
        self.moveSpeed = 5
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -=self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x +=self.moveSpeed
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 10"
        self.center = (500, 30)        
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("Ocean.png")
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 10
        self.score = 0
        
        
        self.sndWorm = simpleGE.Sound("Bubble.mp3")
        
        self.fish = Fish(self)
        self.numWorms = 10
        self.worms = []
        for i in range(self.numWorms):
            self.worms.append(Worm(self))
            
        self.lblScore = LblScore()
        self.lblTime = LblTime()    
            
        self.sprites = [self.fish,
                        self.worms,
                        self.lblScore,
                        self.lblTime]
        
    def process(self):
        for worm in self.worms:
            if worm.collidesWith(self.fish):
                self.sndWorm.play()
                worm.reset()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"Final Score: {self.score}")
            self.stop()           
        
        
class Instructions(simpleGE.Scene):
    def __init__(self, score):
        super().__init__()
        self.setImage("Ocean.png")
        
        self.response = "Play"
        
        self.instructions = simpleGE.MultiLabel()
        self.instructions.textLines = [
        "You are Carl the fish.",
        "Move with the left and right arrow keys",
        "and eat as many worms as you can handle",
        "in only ten seconds!",
        "",
        "Have fun!"]
        
        self.instructions.center = (320, 240)
        self.instructions.size = (500, 250)
        
        self.prevScore = score
        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Last score: {self.prevScore}"
        self.lblScore.center = (320, 400)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play (up)"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit (down)"
        self.btnQuit.center = (550, 400)
        
        self.sprites = [self.instructions,
                        self.lblScore,
                        self.btnQuit,
                        self.btnPlay]
        
    def process(self):
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()

        if self.isKeyPressed(pygame.K_UP):
            self.response = "Play"
            self.stop()
        if self.isKeyPressed(pygame.K_DOWN):
            self.response = "Quit"
            self.stop()

def main():
    keepGoing = True
    score = 0
    while keepGoing:
        
        instructions = Instructions(score)
        instructions.start()
                
        if instructions.response == "Play":    
            game = Game()
            game.start()
            score = game.score
        else:
            keepGoing = False
            
            
if __name__ == "__main__":
    main()