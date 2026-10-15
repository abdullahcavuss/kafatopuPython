import pygame
import math

GROUND_Y = 550  # Ayakkabının alt taban seviyesi
PLAYER_HEAD_W = 50
PLAYER_HEAD_H = 66
SHOE_W = 45
SHOE_H = 20

class Player:
    def __init__(self, x, facing=1, is_ai=False, tint_color=None):
        """
        x: Başlangıç x koordinatı
        facing: 1 (sağa bakan / Sol Oyuncu), -1 (sola bakan / Sağ Oyuncu)
        is_ai: Bilgisayar kontrolünde mi?
        tint_color: İsteğe bağlı renk tonu (Örn: (255, 100, 100) for Player 2)
        """
        self.start_x = x
        self.x = float(x)
        self.y = float(GROUND_Y - PLAYER_HEAD_H - SHOE_H)  # ~464
        self.vx = 0.0
        self.vy = 0.0
        self.facing = facing
        self.is_ai = is_ai
        self.tint_color = tint_color
        
        # Fizik parametreleri
        self.speed = 5.8
        self.jump_power = -13.5
        self.gravity = 0.65
        self.is_grounded = True
        
        # Şut animasyonu durumu
        self.kicking = False
        self.kick_timer = 0
        self.kick_duration = 12  # Frame süresi
        self.kick_cooldown = 0
        
        # Görselleri yükle ve hazırla
        self._load_sprites()
        
    def _load_sprites(self):
        base_head = pygame.image.load('alper.png').convert_alpha()
        base_shoe = pygame.image.load('ayakkabi.png').convert_alpha()
        
        # İkinci oyuncu için renk tonlaması uygula
        if self.tint_color:
            tinted_head = base_head.copy()
            # Renk filtresi: forma/saç ayrımı için kırmızımsı/altın ton
            tint_surf = pygame.Surface(base_head.get_size(), pygame.SRCALPHA)
            tint_surf.fill((*self.tint_color, 75))
            tinted_head.blit(tint_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            base_head = tinted_head
            
            tinted_shoe = base_shoe.copy()
            tint_shoe_surf = pygame.Surface(base_shoe.get_size(), pygame.SRCALPHA)
            tint_shoe_surf.fill((*self.tint_color, 90))
            tinted_shoe.blit(tint_shoe_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            base_shoe = tinted_shoe

        # Eğer sola bakıyorsa yatay olarak çevir
        if self.facing == -1:
            self.head_img = pygame.transform.flip(base_head, True, False)
            self.shoe_img = pygame.transform.flip(base_shoe, True, False)
        else:
            self.head_img = base_head
            self.shoe_img = base_shoe
            
        self.head_rect = self.head_img.get_rect()
        self.shoe_rect = self.shoe_img.get_rect()

    def reset(self):
        self.x = float(self.start_x)
        self.y = float(GROUND_Y - PLAYER_HEAD_H - SHOE_H)
        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = True
        self.kicking = False
        self.kick_timer = 0
        self.kick_cooldown = 0

    def move(self, dir_x):
        self.vx = dir_x * self.speed

    def stop_x(self):
        self.vx = 0.0

    def jump(self, sound_fx=None):
        if self.is_grounded:
            self.vy = self.jump_power
            self.is_grounded = False
            if sound_fx:
                sound_fx.play('jump')

    def shoot(self, sound_fx=None):
        if self.kick_cooldown <= 0:
            self.kicking = True
            self.kick_timer = self.kick_duration
            self.kick_cooldown = 18

    def update(self):
        # Yatay hareket
        self.x += self.vx
        
        # Saha sınırları
        min_x = 20
        max_x = 800 - 20 - PLAYER_HEAD_W
        if self.x < min_x:
            self.x = min_x
        elif self.x > max_x:
            self.x = max_x

        # Düşey hareket ve yerçekimi
        self.vy += self.gravity
        self.y += self.vy
        
        ground_limit = GROUND_Y - PLAYER_HEAD_H - SHOE_H
        if self.y >= ground_limit:
            self.y = ground_limit
            self.vy = 0.0
            self.is_grounded = True

        # Şut animasyonu sayacı
        if self.kick_timer > 0:
            self.kick_timer -= 1
            if self.kick_timer <= 0:
                self.kicking = False
                
        if self.kick_cooldown > 0:
            self.kick_cooldown -= 1

    def get_head_circle(self):
        """Kafa çarpışması için merkez ve yarıçap döndürür"""
        cx = self.x + PLAYER_HEAD_W / 2
        cy = self.y + 28
        radius = 24
        return cx, cy, radius

    def get_kick_hitbox(self):
        """Şut anındaki vuruş alanını döndürür"""
        if not self.kicking:
            return None
        # Vuruş alanı oyuncunun önünde ve ayakkabı hizasında
        if self.facing == 1:
            return pygame.Rect(self.x + 25, self.y + 40, 45, 45)
        else:
            return pygame.Rect(self.x - 20, self.y + 40, 45, 45)

    def draw(self, surface):
        # 1. Baş Çizimi
        surface.blit(self.head_img, (int(self.x), int(self.y)))
        
        # 2. Ayakkabı Çizimi
        # Normal durumda ayakkabı başın biraz altında
        base_shoe_x = self.x + (15 if self.facing == 1 else -10)
        base_shoe_y = self.y + PLAYER_HEAD_H - 4
        
        if self.kicking:
            # Şut vururken ayağı döndür ve öne uzat
            progress = (self.kick_duration - self.kick_timer) / self.kick_duration
            # Sinüs dalgası şeklinde ileri gidip geri gelir
            kick_swing = math.sin(progress * math.pi)
            
            angle = kick_swing * 55 * self.facing
            offset_x = kick_swing * 22 * self.facing
            offset_y = -kick_swing * 12
            
            rotated_shoe = pygame.transform.rotate(self.shoe_img, angle)
            rot_rect = rotated_shoe.get_rect(center=(
                base_shoe_x + SHOE_W / 2 + offset_x,
                base_shoe_y + SHOE_H / 2 + offset_y
            ))
            surface.blit(rotated_shoe, rot_rect.topleft)
        else:
            # Hafif zıplama/koşma salınımı
            walk_bounce = math.sin(pygame.time.get_ticks() * 0.015) * 2 if abs(self.vx) > 0 and self.is_grounded else 0
            surface.blit(self.shoe_img, (int(base_shoe_x), int(base_shoe_y + walk_bounce)))
