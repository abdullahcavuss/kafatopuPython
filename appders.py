import pygame
pygame.init()
class Player(object):
    def __init__(self):
        self.player_x = 100
        self.player_y = 470
        self.playerImg = pygame.image.load('alper.png')
    def yenile(self):
        gameDisplay.blit(self.playerImg,(self.player_x,self.player_y))
    def move(self,dx):
        self.player_x += dx 
    
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('kafaTopu')
clock = pygame.time.Clock()
bg = pygame.image.load("env.jpg")
alper = Player()
crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    gameDisplay.blit(bg,(0, 0))
    alper.yenile()
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        alper.move(-2,0)
    if key[pygame.K_RIGHT]:
        alper.move(2,0)
    if (key[pygame.K_UP]):
        alper.jump()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()
