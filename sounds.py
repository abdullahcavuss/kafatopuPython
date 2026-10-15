import pygame
import math
import struct

class SoundEffects:
    def __init__(self):
        self.enabled = True
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1)
            self._generate_sounds()
        except Exception as e:
            print(f"Ses sistemi başlatılamadı: {e}")
            self.enabled = False

    def _create_sound(self, generator, duration):
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            val = generator(t, i, n_samples)
            sample = int(val * 32767 * 0.5)
            buf += struct.pack('<h', max(-32768, min(32767, sample)))
        return pygame.mixer.Sound(buffer=bytes(buf))

    def _generate_sounds(self):
        # 1. Top Vuruşu (Tok ses)
        def kick_gen(t, i, n):
            f = 140 - 90 * (i / n)
            decay = (1.0 - i / n) ** 2
            return math.sin(2 * math.pi * f * t) * decay

        # 2. Sert Şut (Daha güçlü ve hızlı)
        def shoot_gen(t, i, n):
            f = 220 - 150 * (i / n)
            decay = (1.0 - i / n) ** 1.5
            noise = (math.sin(2 * math.pi * 500 * t) * 0.3) if i < n * 0.3 else 0
            return (math.sin(2 * math.pi * f * t) + noise) * decay

        # 3. Direk Çarpması (Metalik çınlama)
        def post_gen(t, i, n):
            decay = (1.0 - i / n) ** 0.8
            v1 = math.sin(2 * math.pi * 987 * t)
            v2 = math.sin(2 * math.pi * 1320 * t) * 0.6
            return (v1 + v2) * 0.6 * decay

        # 4. Hakem Düdüğü (Çift tonlu titreşim)
        def whistle_gen(t, i, n):
            f = 2400 + 150 * math.sin(2 * math.pi * 25 * t)
            fade_in = min(1.0, i / (n * 0.1))
            fade_out = min(1.0, (n - i) / (n * 0.15))
            return math.sin(2 * math.pi * f * t) * fade_in * fade_out * 0.4

        # 5. Zıplama
        def jump_gen(t, i, n):
            f = 200 + 350 * (i / n)
            decay = (1.0 - i / n)
            return math.sin(2 * math.pi * f * t) * decay * 0.35

        # 6. Gol Efekti (Zafer melodisi / arpej)
        def goal_gen(t, i, n):
            # 4 aşamalı yükselen zafer tonu
            phase = int((i / n) * 4)
            freqs = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
            f = freqs[min(phase, 3)]
            sub_t = t % 0.15
            envelope = math.exp(-sub_t * 6)
            return math.sin(2 * math.pi * f * t) * envelope * 0.5

        self.snd_kick = self._create_sound(kick_gen, 0.12)
        self.snd_shoot = self._create_sound(shoot_gen, 0.15)
        self.snd_post = self._create_sound(post_gen, 0.25)
        self.snd_whistle = self._create_sound(whistle_gen, 0.4)
        self.snd_jump = self._create_sound(jump_gen, 0.12)
        self.snd_goal = self._create_sound(goal_gen, 0.6)

    def play(self, sound_name):
        if not self.enabled:
            return
        snd = getattr(self, f"snd_{sound_name}", None)
        if snd:
            snd.play()
