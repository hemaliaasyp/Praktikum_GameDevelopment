import pygame, sys, time
from pygame.locals import *
from pygame import rect

# Mengatur size dan title untuk window
Width, Height = 400, 400
Title = "Smooth Movement"

# Membuat class Player
class Player:
    # Fungsi untuk menginisialisasi variabel - variabel yang nanti akan digunakan
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.color = (250, 120, 60)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4

    # Fungsi/Perintah untuk menampilkan objek
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    # Fungsi/Perintah untuk meng-update
    def update(self):
        # Mengatur arah gerak objek yang bergerak ke kanan dan ke kiri (horizontal)
        self.velX = 0
        # Mengatur arah gerak objek yang bergerak ke atas dan ke bawah (vertical)
        self.velY = 0

        if self.left_pressed and not self.right_pressed:
            if self.x > 0: # Memberikan batasan agar objek tidak bergerak ke kiri melewati batas ketika tombol panah ke kiri di tekan
                self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            if self.x < 400 - 32: # Memberikan batasan agar objek tidak bergerak ke kanan melewati batas ketika tombol panah ke kanan di tekan
                self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            if self.y > 0: # Memberikan batasan agar objek tidak bergerak ke atas melewati batas ketika tombol panah ke atas di tekan
                self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            if self.y < 400 - 32: # Memberikan batasan agar objek tidak bergerak ke bawah melewati batas ketika tombol panah ke bawah di tekan
                self.velY = self.speed

        self.x += self.velX
        self.y += self.velY

        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)

# Menginisialisasi semua modul yang diperlukan untuk PyGame
pygame.init()
# Membuat variabel win untuk membuat window/layar dengan size yang sudah ditentukan sebelumnya
win = pygame.display.set_mode((Width, Height))
# Menampilkan title atau judul di window/layar
pygame.display.set_caption(Title)
# Men-setting waktu yang diperlukan saat player/objek bergerak
clock = pygame.time.Clock()

# Membuat variabel player untuk mengakses class Plyaer
player = Player(Width/2, Height/2)
# Mengatur warna font
font_color = (0, 150, 250)
# Mengatur style dan size pada font
font = pygame.font.Font(None, 40)
# Menampilkan text dengan warna font yang sudah diatur sebelumnya
text = font.render("Ardianita Fauziyah", True, font_color)

# Apabila program bernilai true maka program akan di running
running = True

# Ketika bernilai benar maka program akan mengeksekusi perintah perintah di bawah ini.
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left_pressed = True
            if event.key == pygame.K_RIGHT:
                player.right_pressed = True
            if event.key == pygame.K_UP:
                player.up_pressed = True
            if event.key == pygame.K_DOWN:
                player.down_pressed = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left_pressed = False
            if event.key == pygame.K_RIGHT:
                player.right_pressed = False
            if event.key == pygame.K_UP:
                player.up_pressed = False
            if event.key == pygame.K_DOWN:
                player.down_pressed = False

    # Mengatur warna/background color window/layar
    win.fill((12, 24, 36))
    # Menampilkan objek rectangle dengan warna putih
    pygame.draw.rect(win, (255,255,255), player)
    # Menampilkan text dengan posisi x = 70 dan y = 30
    win.blit(text,(70, 30))
    # Meng-update player
    player.update()
    # Meng-update tampilan window/layar
    pygame.display.flip()
    # Men-setting lama waktu yang digunakan ketika objek bergerak
    clock.tick(120)
    # Meng-update tampilan window/layar
    pygame.display.update()
