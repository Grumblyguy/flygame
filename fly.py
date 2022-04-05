import os, time, random
import sys, select
import pygame
from pygame.locals import *

class Pipe:
    def __init__(self, startingHeight):
        self.startingHeight = startingHeight
        self.passedPlayer = False
        # Starts at the end of the board
        self.renderBlocks = [[1200,x] for x in range(29)] + [[1170,x] for x in range(29)] + [[1140,x] for x in range(29)]
        toRemove = []
        self.hitbox = [[1140, startingHeight*30],[1230, startingHeight*30],[1140, (startingHeight+5)*30],[1230, (startingHeight+5)*30]]
        for pos in self.renderBlocks:
            if pos[1] >= self.startingHeight and pos[1] <= self.startingHeight + 4:
                toRemove.append(pos)
        for gap in toRemove:
            self.renderBlocks.remove(gap)
    
    def tick(self):
        for pos in self.renderBlocks:
            pos[0] -=5
        for pos in self.hitbox:
            pos[0] -=5
                
class Bird:
    def __init__(self):
        self.acceleration = 0
        self.pos = [600, 450]
        self.hitbox = [[600,450], [630,450], [600,480],[630, 480]]
        self.score = 0

    def jump(self):
        self.acceleration = 20

    def tick(self):
        self.acceleration-=2
        self.pos[1] -= self.acceleration
        for hitbox in self.hitbox:
            hitbox[1] -= self.acceleration
        
class Fly:
    def __init__(self):
        self.tick = 0
        self.pipes = []
        self.player = Bird()
        self.running = False
        self.startScreen = True

    def loadResources(self):
        self.bg = pygame.image.load("resources/back.png")
        self.bg = pygame.transform.scale(self.bg, (1200,900))
        self.deathBg = pygame.image.load("resources/youDied.jpg")
        self.deathBg = pygame.transform.scale(self.deathBg, (1000,500))
        self.playerBlock = pygame.image.load("resources/stone.png").convert()
        self.playerBlock = pygame.transform.scale(self.playerBlock, (30,30))
        self.foodBlock = pygame.image.load("resources/bird.png")
        self.foodBlock = pygame.transform.scale(self.foodBlock, (30,30))
        self.stone = pygame.image.load("resources/pipe.png").convert()
        self.stone = pygame.transform.scale(self.stone, (30,30))

        self.obsidian = pygame.image.load("resources/bg.jpg").convert()
        self.obsidian = pygame.transform.scale(self.obsidian, (1200,90))
        

        self.loadHiScore()

    def renderPipes(self):
        for pipe in self.pipes:
            for pos in pipe.renderBlocks:
                self.surface.blit(self.stone, (pos[0], pos[1]*30))


    def updateEntities(self):
        for pipe in self.pipes:
            pipe.tick()

        if self.tick % 55 == 0:
            self.pipes.append(Pipe(random.randint(2,27)))      
        self.player.tick()
        for pipe in self.pipes:
            if not pipe.passedPlayer:
                if self.player.hitbox[1][0] >= pipe.hitbox[0][0] and self.player.hitbox[0][0] < pipe.hitbox[1][0] \
                    and (self.player.hitbox[0][1] <= pipe.hitbox[0][1] or self.player.hitbox[2][1] >= pipe.hitbox[2][1]):
                    # You died
                    self.running = False
                    if self.player.score > self.hiscore:
                        self.saveHiScore(self.player.score)
                elif self.player.hitbox[0][0] > pipe.hitbox[1][0]:
                    # Pipe has passed player
                    pipe.passedPlayer = True
                    self.player.score+=1

    def renderPlayer(self):
        self.surface.blit(self.foodBlock, (self.player.pos[0], self.player.pos[1]))

    def loadHiScore(self):
        with open('hiscore.txt') as file:
            self.hiscore = int(file.readline())

    def saveHiScore(self, newScore):
        with open('hiscore.txt', 'w') as file:
            file.write(str(newScore))

    def updateBoard(self):
        self.surface.fill((255,255,255))
        if self.running:
            self.updateEntities()
        self.renderBackground()
        self.renderPipes()
        self.renderPlayer()
        self.renderUI()
        pygame.display.flip()
    
    def renderBackground(self):
        self.surface.blit(self.bg, (0,0))
    
    def renderUI(self):
        playerscore = self.comicsans.render(f'Score: {self.player.score}', False, (255, 255, 255))
        hiscore = self.comicsans.render(f'High Score: {self.hiscore}', False, (255, 255, 255))
        self.surface.blit(playerscore, (20,20))
        self.surface.blit(hiscore, (20,60))

        if not self.running:
            if self.startScreen:
                self.surface.blit(self.obsidian, (0, 380))
                playAgain = self.comicsans.render(f'Copywright free flying bird game (Space to start)', False, (255, 255, 255))
                self.surface.blit(playAgain, (300,400))
            else:
                playAgain = self.comicsans.render(f'Play again? (Space)', False, (255, 255, 255))
                self.surface.blit(playAgain, (500,400))

    def run(self):
        pygame.init()
        self.comicsans = pygame.font.SysFont('Comic Sans MS', 30)
        self.surface = pygame.display.set_mode((1200,900))
        self.loadResources()
        self.updateBoard()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.locals.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE and self.running:
                        self.player.jump()
                    elif event.key == K_SPACE and not self.running:
                        self.player = Bird()
                        self.pipes = []
                        self.loadHiScore()
                        self.running = True
                        self.startScreen = False
                elif event.type == QUIT:
                    running = False
            self.tick+=1
            self.updateBoard()
            time.sleep(0.05)

game = Fly()
game.run()