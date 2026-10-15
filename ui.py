import pygame
import math
import random

class UI:
    def __init__(self):
        pygame.font.init()
        # Sistem fontlarını seç
        self.font_large = pygame.font.SysFont('Arial', 54, bold=True)
        self.font_score = pygame.font.SysFont('Arial', 40, bold=True)
        self.font_mid = pygame.font.SysFont('Arial', 26, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 18, bold=True)
        
        # Gol kutlaması için konfetiler
        self.confetti = []

    def draw_scoreboard(self, surface, score1, score2, time_left, p1_name="OYUNCU 1", p2_name="BİLGİSAYAR"):
        # Üst Panel Kutusu
        panel_w = 420
        panel_h = 60
        panel_x = (800 - panel_w) // 2
        panel_y = 10
        
        # Yarı saydam arka plan
        board_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        board_surf.fill((20, 20, 25, 210))
        surface.blit(board_surf, (panel_x, panel_y))
        
        # Kenarlık çizgisi
        pygame.draw.rect(surface, (230, 230, 230), (panel_x, panel_y, panel_w, panel_h), width=2, border_radius=6)
        
        # Süre Kutusu (Ortada)
        time_text = f"{max(0, int(time_left)):02d}"
        time_render = self.font_score.render(time_text, True, (255, 230, 60))
        surface.blit(time_render, (400 - time_render.get_width() // 2, panel_y + 8))

        # Oyuncu 1 Skoru ve İsmi (Sol)
        s1_render = self.font_score.render(str(score1), True, (80, 190, 255))
        surface.blit(s1_render, (panel_x + 90, panel_y + 8))
        
        name1_render = self.font_small.render(p1_name, True, (200, 230, 255))
        surface.blit(name1_render, (panel_x + 15, panel_y + 20))

        # Oyuncu 2 Skoru ve İsmi (Sağ)
        s2_render = self.font_score.render(str(score2), True, (255, 100, 100))
        surface.blit(s2_render, (panel_x + panel_w - 90 - s2_render.get_width(), panel_y + 8))
        
        name2_render = self.font_small.render(p2_name, True, (255, 210, 210))
        surface.blit(name2_render, (panel_x + panel_w - 15 - name2_render.get_width(), panel_y + 20))

    def trigger_goal_fx(self):
        self.confetti.clear()
        colors = [(255, 50, 50), (50, 255, 50), (50, 150, 255), (255, 255, 50), (255, 150, 255), (255, 255, 255)]
        for _ in range(70):
            self.confetti.append({
                'x': random.uniform(100, 700),
                'y': random.uniform(-40, 150),
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(2, 6),
                'size': random.uniform(4, 9),
                'color': random.choice(colors)
            })

    def draw_goal_animation(self, surface, goal_timer_ratio):
        # Konfetileri güncelle ve çiz
        for c in self.confetti:
            c['x'] += c['vx']
            c['y'] += c['vy']
            pygame.draw.rect(surface, c['color'], (int(c['x']), int(c['y']), int(c['size']), int(c['size'])))

        # Büyüyen GOOOL yazısı
        pulse = 1.0 + 0.15 * math.sin(pygame.time.get_ticks() * 0.015)
        text = "G O O O O L !"
        
        # Gölge
        shadow = self.font_large.render(text, True, (10, 10, 10))
        scaled_s = pygame.transform.rotozoom(shadow, 0, pulse)
        surface.blit(scaled_s, scaled_s.get_rect(center=(403, 223)))
        
        # Parlak Yazı
        txt_render = self.font_large.render(text, True, (255, 235, 40))
        scaled = pygame.transform.rotozoom(txt_render, 0, pulse)
        surface.blit(scaled, scaled.get_rect(center=(400, 220)))

    def draw_game_over(self, surface, score1, score2, p1_name, p2_name):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        # Başlık
        title = self.font_large.render("MAÇ BİTTİ!", True, (255, 230, 70))
        surface.blit(title, title.get_rect(center=(400, 170)))

        # Kazanan Mesajı
        if score1 > score2:
            win_text = f"{p1_name} KAZANDI!"
            win_col = (80, 200, 255)
        elif score2 > score1:
            win_text = f"{p2_name} KAZANDI!"
            win_col = (255, 100, 100)
        else:
            win_text = "MAÇ BERABERE!"
            win_col = (230, 230, 230)
            
        win_render = self.font_score.render(win_text, True, win_col)
        surface.blit(win_render, win_render.get_rect(center=(400, 250)))

        # Son Skor
        score_txt = f"{score1}  -  {score2}"
        score_render = self.font_large.render(score_txt, True, (255, 255, 255))
        surface.blit(score_render, score_render.get_rect(center=(400, 320)))

        # Kontrol İpuçları
        tip1 = self.font_mid.render("[ R ] Tekrar Oyna", True, (120, 255, 120))
        surface.blit(tip1, tip1.get_rect(center=(400, 410)))
        
        tip2 = self.font_mid.render("[ ESC ] Ana Menüye Dön", True, (255, 180, 100))
        surface.blit(tip2, tip2.get_rect(center=(400, 460)))

    def draw_menu(self, surface, selected_idx):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((10, 15, 30, 200))
        surface.blit(overlay, (0, 0))

        # Logo / Başlık
        title = self.font_large.render("KAFA TOPU", True, (255, 220, 40))
        surface.blit(title, title.get_rect(center=(400, 130)))
        
        subtitle = self.font_small.render("6 Yıl Sonra Efsane Geri Döndü!", True, (180, 210, 255))
        surface.blit(subtitle, subtitle.get_rect(center=(400, 180)))

        # Seçenekler
        options = [
            "1. Tek Kişilik (vs Bilgisayar)",
            "2. İki Kişilik (1v1 Karşılıklı)",
            "3. Kontroller & Nasıl Oynanır",
            "4. Çıkış"
        ]

        for i, opt in enumerate(options):
            is_selected = (i == selected_idx)
            color = (255, 240, 80) if is_selected else (220, 220, 220)
            prefix = "▶  " if is_selected else "   "
            txt = self.font_mid.render(prefix + opt, True, color)
            rect = txt.get_rect(center=(400, 260 + i * 55))
            
            if is_selected:
                # Arka plan vurgusu
                highlight = pygame.Surface((rect.width + 40, rect.height + 12), pygame.SRCALPHA)
                highlight.fill((255, 255, 255, 30))
                surface.blit(highlight, highlight.get_rect(center=rect.center))
                
            surface.blit(txt, rect)

        hint = self.font_small.render("Yukarı / Aşağı Ok ile seç, ENTER ile Başlat", True, (160, 170, 190))
        surface.blit(hint, hint.get_rect(center=(400, 530)))

    def draw_controls_overlay(self, surface):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((15, 20, 35, 235))
        surface.blit(overlay, (0, 0))

        title = self.font_large.render("KONTROLLER", True, (255, 225, 50))
        surface.blit(title, title.get_rect(center=(400, 100)))

        # P1 Kontrolleri Kutusu
        pygame.draw.rect(surface, (60, 120, 200), (80, 170, 300, 260), width=2, border_radius=8)
        p1_title = self.font_mid.render("1. OYUNCU (SOL)", True, (80, 190, 255))
        surface.blit(p1_title, (120, 190))
        p1_lines = [
            "A / D : Sol / Sağ",
            "W : Zıplama",
            "BOŞLUK (Space) : Şut",
            "(Tek kişiliktir: Ok tuşları da çalışır)"
        ]
        for idx, line in enumerate(p1_lines):
            t = self.font_small.render(line, True, (220, 235, 255))
            surface.blit(t, (100, 245 + idx * 35))

        # P2 Kontrolleri Kutusu
        pygame.draw.rect(surface, (200, 80, 80), (420, 170, 300, 260), width=2, border_radius=8)
        p2_title = self.font_mid.render("2. OYUNCU (SAĞ)", True, (255, 110, 110))
        surface.blit(p2_title, (460, 190))
        p2_lines = [
            "Sol / Sağ Ok : Hareket",
            "Yukarı Ok : Zıplama",
            "Aşağı Ok / Enter : Şut",
            "(vs Bilgisayar modunda AI oynar)"
        ]
        for idx, line in enumerate(p2_lines):
            t = self.font_small.render(line, True, (255, 225, 225))
            surface.blit(t, (440, 245 + idx * 35))

        back_hint = self.font_mid.render("Geri dönmek için [ ESC ] veya [ ENTER ]'a basın", True, (255, 240, 100))
        surface.blit(back_hint, back_hint.get_rect(center=(400, 490)))
