import pygame
import math
import random

GROUND_Y = 550
GOAL_TOP_Y = 392
LEFT_POST_X = 92
RIGHT_POST_X = 708

class Ball:
    def __init__(self, x=400, y=280):
        self.start_x = float(x)
        self.start_y = float(y)
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.radius = 18.0
        
        # Fizik parametreleri
        self.gravity = 0.42
        self.bounce = 0.75
        self.friction = 0.985
        self.max_speed = 22.0
        
        # Görsel parametreler
        self.img = pygame.image.load('ball.png').convert_alpha()
        self.angle = 0.0
        
        # Gol durumu
        self.in_goal = None  # 'left' veya 'right'
        
        # Parçacık izleri (sert vuruş efekti)
        self.particles = []

    def reset(self, serve_direction=0):
        self.x = self.start_x
        self.y = self.start_y
        # Hafif yönlü servis
        self.vx = serve_direction * 2.5
        self.vy = -3.0
        self.in_goal = None
        self.particles.clear()

    def update(self, sound_fx=None):
        # Hız sınırlandırması
        speed = math.hypot(self.vx, self.vy)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.vx *= scale
            self.vy *= scale

        # Hızlı gidiyorsa arkasında iz parçacığı bırak
        if speed > 10.0:
            self.particles.append([self.x, self.y, 4, (255, 255, 200, 180)])

        # Parçacıkları güncelle
        for p in self.particles:
            p[2] -= 0.3  # Yarıçap azalır
        self.particles = [p for p in self.particles if p[2] > 0]

        # Yerçekimi
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        # Topun dönme açısı
        self.angle -= self.vx * 3.5

        # 1. Zemin ile Çarpışma
        if self.y + self.radius >= GROUND_Y:
            self.y = GROUND_Y - self.radius
            if abs(self.vy) > 1.2:
                self.vy = -self.vy * self.bounce
                if sound_fx and abs(self.vy) > 2.5:
                    sound_fx.play('kick')
            else:
                self.vy = 0
            self.vx *= self.friction

        # 2. Tavan ile Çarpışma
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = -self.vy * self.bounce

        # 3. Kaleler ve Direkler
        # Sol Direk Köşesi (LEFT_POST_X, GOAL_TOP_Y)
        self._check_post_collision(LEFT_POST_X, GOAL_TOP_Y, sound_fx)
        # Sağ Direk Köşesi (RIGHT_POST_X, GOAL_TOP_Y)
        self._check_post_collision(RIGHT_POST_X, GOAL_TOP_Y, sound_fx)

        # Üst Direk Yatay Çubuğu Çarpışması
        if self.y + self.radius >= GOAL_TOP_Y - 4 and self.y - self.radius <= GOAL_TOP_Y + 4:
            # Sol kale üst direk üstü
            if self.x <= LEFT_POST_X:
                self.y = GOAL_TOP_Y - self.radius - 2
                self.vy = -abs(self.vy) * self.bounce
                if sound_fx:
                    sound_fx.play('post')
            # Sağ kale üst direk üstü
            elif self.x >= RIGHT_POST_X:
                self.y = GOAL_TOP_Y - self.radius - 2
                self.vy = -abs(self.vy) * self.bounce
                if sound_fx:
                    sound_fx.play('post')

        # 4. Yan Duvarlar & Gol Kontrolü
        # Sol Kale ve Duvar
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = -self.vx * 0.4
        elif self.x <= LEFT_POST_X:
            # Direk hizasından içeride
            if self.y > GOAL_TOP_Y + 5:
                # Gol oldu! Sol kaleye girdi
                if not self.in_goal:
                    self.in_goal = 'left'
            else:
                # Direk üstündeyse geri seker
                if self.x - self.radius <= 0:
                    self.x = self.radius
                    self.vx = -self.vx * self.bounce

        # Sağ Kale ve Duvar
        if self.x + self.radius >= 800:
            self.x = 800 - self.radius
            self.vx = -self.vx * 0.4
        elif self.x >= RIGHT_POST_X:
            # Direk hizasından içeride
            if self.y > GOAL_TOP_Y + 5:
                # Gol oldu! Sağ kaleye girdi
                if not self.in_goal:
                    self.in_goal = 'right'
            else:
                if self.x + self.radius >= 800:
                    self.x = 800 - self.radius
                    self.vx = -self.vx * self.bounce

    def _check_post_collision(self, post_x, post_y, sound_fx):
        """Direğin köşe noktasıyla daire çarpışması (ding sesiyle seker)"""
        dx = self.x - post_x
        dy = self.y - post_y
        dist = math.hypot(dx, dy)
        if dist < self.radius + 5.0 and dist > 0.001:
            nx = dx / dist
            ny = dy / dist
            # Konum düzelt
            overlap = (self.radius + 5.0) - dist
            self.x += nx * overlap
            self.y += ny * overlap
            
            # Hız yansıt
            vel_along_norm = self.vx * nx + self.vy * ny
            if vel_along_norm < 0:
                impulse = -(1 + self.bounce) * vel_along_norm
                self.vx += impulse * nx
                self.vy += impulse * ny
                if sound_fx:
                    sound_fx.play('post')

    def check_player_collision(self, player, sound_fx=None):
        """Oyuncu ile kafa ve şut çarpışmalarını işler"""
        # 1. Şut Vuruşu Kontrolü
        hitbox = player.get_kick_hitbox()
        if hitbox:
            # Topun merkezi vuruş kutusunda mı veya yakın mı?
            ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
            if hitbox.colliderect(ball_rect):
                # Süper Vuruş!
                power_x = 16.5 * player.facing
                power_y = -7.5 - random.uniform(0.5, 2.5)
                self.vx = power_x
                self.vy = power_y
                self.x += player.facing * 15
                if sound_fx:
                    sound_fx.play('shoot')
                return

        # 2. Kafa Çarpışması
        head_x, head_y, head_r = player.get_head_circle()
        dx = self.x - head_x
        dy = self.y - head_y
        dist = math.hypot(dx, dy)
        min_dist = self.radius + head_r

        if dist < min_dist and dist > 0.001:
            nx = dx / dist
            ny = dy / dist
            
            # Pozisyon ayrıştırma
            overlap = min_dist - dist
            self.x += nx * overlap
            self.y += ny * overlap
            
            # Göreceli hız
            rvx = self.vx - player.vx
            rvy = self.vy - player.vy
            vel_along_norm = rvx * nx + rvy * ny
            
            if vel_along_norm < 0:
                impulse = -(1 + self.bounce) * vel_along_norm
                self.vx += impulse * nx + player.vx * 0.5
                self.vy += impulse * ny + player.vy * 0.5
                
                # Asgari sekme garantisi
                if abs(self.vx) < 3.0:
                    self.vx = 4.0 * (1 if nx > 0 else -1)
                if sound_fx:
                    sound_fx.play('kick')

    def draw(self, surface):
        # 1. Parçacık izlerini çiz
        for px, py, pr, col in self.particles:
            s = pygame.Surface((int(pr * 2), int(pr * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, col, (int(pr), int(pr)), int(pr))
            surface.blit(s, (int(px - pr), int(py - pr)))

        # 2. Döndürülmüş top görselini çiz
        rotated = pygame.transform.rotate(self.img, self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect.topleft)
