<div align="center">

# ⚽ Kafa Topu Python (Head Ball) 🎮

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6+-yellow?style=for-the-badge&logo=python)](https://www.pygame.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Durum-Tamamlandı-success?style=for-the-badge)]()

**6 yıl önce temelleri atılan nostaljik Kafa Topu projesi; modern fizik motoru, yapay zeka rakibi, dahili ses efektleri ve 2 kişilik moduyla küllerinden yeniden doğdu!**

[Özellikler](#-özellikler) • [Kontroller](#-kontroller) • [Kurulum](#-kurulum) • [Proje Yapısı](#-proje-yapısı)

</div>

---

## 📖 Hikaye

Bu proje 2020 yılında ilk temelleri atılmış, ancak yarım kalmış bir Kafa Topu klonuydu. 6 yıl aradan sonra oyun baştan sona elden geçirilerek eksik olan top ve kale fizikleri, zıplama ve şut animasyonları, akıllı bir yapay zeka rakip ve dahili ses sistemi eklenerek eksiksiz bir arcade futbol oyununa dönüştürüldü.

---

## ✨ Özellikler

- ⚽ **Gelişmiş Top Fiziği**: Gerçekçi yerçekimi, hava sürtünmesi, zemin sekmesi ve falso/spin dönüş mekaniği.
- 👟 **Şut & Kafa Vuruşu Animasyonu**: Boşluk (Space) tuşuna basıldığında ayakkabının savrulmasıyla roket gibi giden şutlar ve açılı kafa vuruşları.
- 🤖 **Yapay Zeka (AI Rakip)**: Tek kişilik modda kaleyi savunan, topun gelişini süzüp havada kafayla karşılayan ve fırsat bulduğunda kaleye şut çeken dinamik yapay zeka.
- 👥 **İki Kişilik (1v1) Mod**: Aynı klavye üzerinden iki arkadaşın karşılıklı mücadele edebileceği rekabetçi mod.
- 🔊 **Prosedürel Ses Sistemi**: Sıfır harici dosya bağımlılığı! Tüm ses efektleri (şut, kafa vuruşu, direk çınlaması, hakem düdüğü, gol sevinci) saf Python algoritmalarıyla anlık sentezlenir.
- 🥅 **Direk ve File Çarpışmaları**: Üst direğin köşesinden metalik sesle seken toplar ve fileye girince tetiklenen gol algısı.
- ⏱️ **Skorboard & Maç Sayacı**: 60 saniyelik maç geri sayımı, anlık skor tabelası ve maç sonu kazanan ekranı.
- 🎉 **Gol Kutlaması**: Gol olduğunda ekranda büyüyen GOOOL yazısı ve renkli konfeti yağmuru.
- 📋 **Kullanıcı Dostu Menüler**: Ana menü, kontroller rehberi ve duraklatma (pause) özellikleri.

---

## 🕹️ Kontroller

| Eylem | 1. Oyuncu (Sol / Mavi) | 2. Oyuncu (Sağ / Kırmızı) |
| :--- | :--- | :--- |
| **Sola Koş** | <kbd>A</kbd> *(Tek kişilikte: <kbd>←</kbd>)* | <kbd>←</kbd> |
| **Sağa Koş** | <kbd>D</kbd> *(Tek kişilikte: <kbd>→</kbd>)* | <kbd>→</kbd> |
| **Zıpla** | <kbd>W</kbd> *(Tek kişilikte: <kbd>↑</kbd>)* | <kbd>↑</kbd> |
| **Şut Çek** | <kbd>Space</kbd> veya <kbd>F</kbd> | <kbd>Enter</kbd> veya <kbd>↓</kbd> |

### Genel Kısayollar
- <kbd>P</kbd> : Oyunu Duraklat / Devam Et
- <kbd>R</kbd> : Maç Bitince Yeniden Başlat (Rövanş)
- <kbd>ESC</kbd> : Ana Menüye Dön / Çıkış

---

## 🚀 Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/kullanici-adiniz/kafatopuPython.git
   cd kafatopuPython
   ```

2. Gerekli kütüphaneyi yükleyin (Sadece `pygame` gereklidir):
   ```bash
   pip install pygame
   ```

3. Oyunu başlatın:
   ```bash
   python app.py
   ```

---

## 📁 Proje Yapısı

```text
kafatopuPython/
│
├── app.py           # Ana oyun döngüsü ve durum yönetimi (Menu, Game, GameOver)
├── player.py        # Oyuncu sınıfı (hareket, zıplama, şut animasyonu, çarpışma)
├── ball.py          # Top fiziği, zemin/direk çarpışmaları, falso ve iz efektleri
├── ai.py            # Bilgisayar rakip (savunma, hücum, zıplama ve şut kararları)
├── ui.py            # Skor tabelası, sayaç, gol animasyonu, menü ve kontroller ekranı
├── sounds.py        # Prosedürel ses sentezleyici (şut, direk, düdük, gol sesleri)
│
├── alper.png        # 1. Oyuncu kafa görseli
├── ayakkabi.png     # Krampon görseli
├── ball.png         # Futbol topu görseli
├── env.jpg          # Stadyum / saha arka planı
├── kaleSol.png      # Sol kale direği ve filesi
├── kaleSag.png      # Sağ kale direği ve filesi
│
├── README.md        # Proje tanıtım ve kullanım kılavuzu
└── .gitignore       # Git için geçici ve gereksiz dosya filtreleri
```

---

## 📜 Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında lisanslanmıştır. Dilediğiniz gibi geliştirebilir, oynayabilir ve paylaşabilirsiniz.
