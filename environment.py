import pygame
pygame.display.set_caption('kafaTopu')
clock = pygame.time.Clock()
class Env(object):
    def __init__(self):
        self.gameDisplay = pygame.display.set_mode((800,600))
        self.bg = pygame.image.load("env.jpg")
        self.crashed = False
    
    def update(self,img,x,y):
        self.gameDisplay.blit(self.bg,(0, 0))
        self.gameDisplay.blit(img,(x,y))
        
