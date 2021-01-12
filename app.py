import pygame
import Playerr
pygame.init()

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('kafaTopu')
clock = pygame.time.Clock()
bg = pygame.image.load("env.jpg")
alper = Playerr.Player()
crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    gameDisplay.blit(bg,(0, 0))
    
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        alper.move(-2,0)
    if key[pygame.K_RIGHT]:
        alper.move(2,0)
    if (key[pygame.K_UP]):
        alper.jump()
    if (key[pygame.K_SPACE]):
        alper.shoot()
    alper.update()
    gameDisplay.blit(alper.playerImg,(alper.player_x,alper.player_y))
    gameDisplay.blit(alper.playerShoesImg,(alper.shoes_x,alper.shoes_y))
    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()