import random
import pygame

class AIController:
    def __init__(self, ai_player, ball, difficulty="normal"):
        self.player = ai_player
        self.ball = ball
        self.difficulty = difficulty
        self.decision_timer = 0
        self.target_x = 640
        self.should_jump = False
        self.should_shoot = False

    def update(self, sound_fx=None):
        self.decision_timer += 1
        
        # Karar sıklığı
        freq = 3 if self.difficulty == "hard" else 6
        if self.decision_timer >= freq:
            self.decision_timer = 0
            self._make_decisions()

        # Yatay Hareket
        dist_x = self.target_x - self.player.x
        if abs(dist_x) > 10:
            if dist_x > 0:
                self.player.move(1)
            else:
                self.player.move(-1)
        else:
            self.player.stop_x()

        # Zıplama
        if self.should_jump and self.player.is_grounded:
            self.player.jump(sound_fx)
            self.should_jump = False

        # Şut
        if self.should_shoot:
            self.player.shoot(sound_fx)
            self.should_shoot = False

    def _make_decisions(self):
        ball_x = self.ball.x
        ball_y = self.ball.y
        player_x = self.player.x
        player_y = self.player.y

        # Savunma veya Hücum Pozisyonu
        if ball_x > 380:
            # Top bizim yarı sahamızda
            # Topun biraz sağına geçmeye çalış ki sola doğru (rakip kaleye) vurabilsin
            self.target_x = ball_x + 22
        else:
            # Top rakip yarı sahada, kale önünde bekle
            self.target_x = 630 + random.randint(-20, 20)

        # Kalenin içine girmeyi önle
        if self.target_x > 710:
            self.target_x = 700
        if self.target_x < 150:
            self.target_x = 150

        # Zıplama Kararı
        dx = abs(ball_x - player_x)
        if dx < 65 and player_y - 85 < ball_y < player_y + 15:
            # Top havadayken kafa vurmak için zıpla
            self.should_jump = True

        # Şut Kararı
        # Top önümüzde ve vuruş hizasındaysa
        if (player_x - 55 < ball_x < player_x) and (ball_y > player_y + 20):
            self.should_shoot = True
