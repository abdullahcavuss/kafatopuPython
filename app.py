import pygame
import sys
from player import Player
from ball import Ball
from sounds import SoundEffects
from ai import AIController
from ui import UI

# Oyun Durumları
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GOAL = 2
STATE_GAME_OVER = 3
STATE_CONTROLS = 4

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MATCH_DURATION = 60  # Saniye

def main():
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=1)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Kafa Topu - Efsane Geri Döndü!")
    clock = pygame.time.Clock()

    # Görselleri Yükle
    bg = pygame.image.load("env.jpg").convert()
    kale_sol = pygame.image.load("kaleSol.png").convert_alpha()
    kale_sag = pygame.image.load("kaleSag.png").convert_alpha()
    
    # Kalelerin Konumları (Zemin y=550, kale h=161 -> y=389)
    GOAL_Y = 389
    left_goal_pos = (0, GOAL_Y)
    right_goal_pos = (SCREEN_WIDTH - kale_sag.get_width(), GOAL_Y)

    # Sesler ve UI
    sounds = SoundEffects()
    ui = UI()

    # Oyun Değişkenleri
    state = STATE_MENU
    menu_selection = 0
    game_mode = "1p"  # "1p" (vs AI) veya "2p" (1v1)
    
    score1 = 0
    score2 = 0
    time_left = MATCH_DURATION
    goal_timer = 0
    paused = False

    # Oyuncular ve Top
    p1 = Player(x=180, facing=1, is_ai=False)
    p2 = Player(x=570, facing=-1, is_ai=True, tint_color=(240, 70, 70))
    ball = Ball(x=400, y=260)
    ai_bot = AIController(p2, ball, difficulty="normal")

    def start_new_match(mode="1p"):
        nonlocal score1, score2, time_left, state, game_mode, p2, ai_bot
        game_mode = mode
        score1 = 0
        score2 = 0
        time_left = MATCH_DURATION
        
        p1.reset()
        p2 = Player(x=570, facing=-1, is_ai=(mode == "1p"), tint_color=(240, 70, 70))
        ai_bot = AIController(p2, ball, difficulty="normal")
        ball.reset(serve_direction=0)
        
        sounds.play("whistle")
        state = STATE_PLAYING

    def reset_after_goal(last_scorer):
        p1.reset()
        p2.reset()
        # Top son golü yiyen takıma doğru hafifçe servis edilir
        serve_dir = 1 if last_scorer == 2 else -1
        ball.reset(serve_direction=serve_dir)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Saniye cinsinden geçen süre

        # ----------------- OLAY DÖNGÜSÜ (EVENTS) -----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                # ANA MENÜ KONTROLLERİ
                if state == STATE_MENU:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        menu_selection = (menu_selection - 1) % 4
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        menu_selection = (menu_selection + 1) % 4
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if menu_selection == 0:
                            start_new_match("1p")
                        elif menu_selection == 1:
                            start_new_match("2p")
                        elif menu_selection == 2:
                            state = STATE_CONTROLS
                        elif menu_selection == 3:
                            running = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

                # KONTROLLER EKRANI
                elif state == STATE_CONTROLS:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                        state = STATE_MENU

                # OYUN İÇİ KONTROLLER
                elif state in (STATE_PLAYING, STATE_GOAL):
                    if event.key == pygame.K_p:
                        paused = not paused
                    elif event.key == pygame.K_ESCAPE:
                        state = STATE_MENU

                    # Player 1 Zıplama & Şut (Keydown anlık basım)
                    if not paused and state == STATE_PLAYING:
                        if event.key in (pygame.K_w, pygame.K_UP if game_mode == "1p" else None):
                            p1.jump(sounds)
                        if event.key in (pygame.K_SPACE, pygame.K_f):
                            p1.shoot(sounds)

                        # Player 2 (Sadece 2 Oyuncu Modunda)
                        if game_mode == "2p":
                            if event.key == pygame.K_UP:
                                p2.jump(sounds)
                            if event.key in (pygame.K_RETURN, pygame.K_DOWN, pygame.K_KP0):
                                p2.shoot(sounds)

                # MAÇ BİTTİ EKRANI
                elif state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        start_new_match(game_mode)
                    elif event.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                        state = STATE_MENU

        # ----------------- OYUN MANTIĞI & GÜNCELLEME -----------------
        if not paused:
            if state == STATE_PLAYING:
                # Süre Sayacı
                time_left -= dt
                if time_left <= 0:
                    time_left = 0
                    sounds.play("whistle")
                    state = STATE_GAME_OVER

                # Sürekli Tuş Basımları (Yatay Hareket)
                keys = pygame.key.get_pressed()
                
                # Player 1 Hareketi
                move_p1 = 0
                if keys[pygame.K_a] or (game_mode == "1p" and keys[pygame.K_LEFT]):
                    move_p1 -= 1
                if keys[pygame.K_d] or (game_mode == "1p" and keys[pygame.K_RIGHT]):
                    move_p1 += 1
                p1.move(move_p1)

                # Player 2 Hareketi
                if game_mode == "2p":
                    move_p2 = 0
                    if keys[pygame.K_LEFT]:
                        move_p2 -= 1
                    if keys[pygame.K_RIGHT]:
                        move_p2 += 1
                    p2.move(move_p2)
                else:
                    # AI Kontrolü
                    ai_bot.update(sounds)

                # Karakter ve Top Güncellemeleri
                p1.update()
                p2.update()
                
                # İki Oyuncunun İtişmesi (Çarpışma)
                dist_players = abs(p1.x - p2.x)
                if dist_players < 40 and abs(p1.y - p2.y) < 50:
                    mid = (p1.x + p2.x) / 2
                    p1.x = mid - 20
                    p2.x = mid + 20

                ball.update(sounds)
                ball.check_player_collision(p1, sounds)
                ball.check_player_collision(p2, sounds)

                # Gol Kontrolü
                if ball.in_goal:
                    if ball.in_goal == "left":
                        # Sol kaleye girdi -> Player 2 Gol Attı!
                        score2 += 1
                        last_scorer = 2
                    else:
                        # Sağ kaleye girdi -> Player 1 Gol Attı!
                        score1 += 1
                        last_scorer = 1
                    
                    sounds.play("goal")
                    ui.trigger_goal_fx()
                    goal_timer = 2.0  # 2 saniye kutlama
                    state = STATE_GOAL

            elif state == STATE_GOAL:
                # Gol Sonrası Bekleme ve Parçacıklar
                goal_timer -= dt
                ball.update(None)
                p1.update()
                p2.update()
                if goal_timer <= 0:
                    sounds.play("whistle")
                    reset_after_goal(last_scorer)
                    state = STATE_PLAYING

        # ----------------- ÇİZİM AŞAMASI (RENDERING) -----------------
        # 1. Arka Plan
        screen.blit(bg, (0, 0))

        # 2. Kaleler (Arka planda kalır, top ve oyuncular kalenin önünden geçer veya içine girer)
        screen.blit(kale_sol, left_goal_pos)
        screen.blit(kale_sag, right_goal_pos)

        # 3. Oyuncular ve Top
        p1.draw(screen)
        p2.draw(screen)
        ball.draw(screen)

        # 4. Arayüz ve Durum Katmanları
        p2_label = "BİLGİSAYAR" if game_mode == "1p" else "OYUNCU 2"
        
        if state in (STATE_PLAYING, STATE_GOAL):
            ui.draw_scoreboard(screen, score1, score2, time_left, "OYUNCU 1", p2_label)
            if state == STATE_GOAL:
                ui.draw_goal_animation(screen, goal_timer / 2.0)
            if paused:
                pause_surf = ui.font_mid.render("OYUN DURAKLATILDI (Devam için P'ye basın)", True, (255, 230, 80))
                screen.blit(pause_surf, pause_surf.get_rect(center=(400, 300)))

        elif state == STATE_MENU:
            ui.draw_menu(screen, menu_selection)

        elif state == STATE_CONTROLS:
            ui.draw_controls_overlay(screen)

        elif state == STATE_GAME_OVER:
            ui.draw_scoreboard(screen, score1, score2, 0, "OYUNCU 1", p2_label)
            ui.draw_game_over(screen, score1, score2, "OYUNCU 1", p2_label)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()