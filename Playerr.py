import pygame

class Player(object):
    speed = 10
    # Stores if player is jumping or not.
    isjump = 0     
    # Force (v) up and mass m.
    v = 8
    m = 4
    def __init__(self):
        self.playerImg = pygame.image.load('alper.png')
        self.playerShoesImg = pygame.image.load('ayakkabi.png')
        self.player_x = 100
        self.player_y = 470
        self.shoes_x = self.player_x + 20
        self.shoes_y = self.player_y + 60 

    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.player_x += dx
        self.player_y += dy
        self.shoes_x = self.player_x + 20
        self.shoes_y = self.player_y + 60 
    
    def vur(self):
        self.playerShoesImg = pygame.transform.rotate(self.playerShoesImg,45)

    def jump(self):
        self.isjump = 1
        print(self.isjump)
    def shoot(self):
        if self.v > 0:
            F = ( 1 * self.m * (self.v*self.v) )
        else:
            F = -( 1 * self.m * (self.v*self.v) )

        # Change position
        self.shoes_y = self.player_y - F
        self.shoes_x= self.player_x + 30

        # Change velocity
        self.v = self.v - 1

        # If ground is reached, reset variables.
        if self.shoes_y >= 470+60:
            self.shoes_y = 470+60
            self.shoes_x = self.player_x + 20
            self.v = 5
        else:
            self.shoes_y= self.player_y - F
            self.shoes_x= self.player_x + F
            
            

    def update(self):
        if self.isjump == 1:
            # Calculate force (F). F = 0.5 * mass * velocity^2.
            if self.v > 0:
                F = ( 0.5 * self.m * (self.v*self.v) )
            else:
                F = -( 0.5 * self.m * (self.v*self.v) )
    
            # Change position
            self.player_y = self.player_y - F
            self.shoes_y = self.player_y + 60 

            # Change velocity
            self.v = self.v - 1

            # If ground is reached, reset variables.
            if self.player_y >= 470:
                self.player_y = 470
                self.isjump = 0
                self.v = 5
        else:
            self.player_y= 470
        





