import pygame
import random

pygame.init()

# Dimensi layar permainan
WIDTH, HEIGHT = 600, 500

# Definisi Palet Warna ala Neon
BLACK = (10, 10, 15)       # Latar belakang gelap kebiruan (nuansa neon)
WHITE = (255, 255, 255)
GREEN = (46, 204, 113)     # Hijau neon
RED = (231, 76, 60)        # Merah neon
YELLOW = (241, 196, 15)    # Kuning (Multi-Ball)
CYAN = (0, 255, 255)       # Cyan / Biru muda (Judul & Lebar Papan)
PURPLE = (155, 89, 182)    # Ungu (Nyawa Tambahan)

font = pygame.font.Font('freesansbold.ttf', 16)
large_font = pygame.font.Font('freesansbold.ttf', 26)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker - Neon Arcade Edition")

# Mengontrol kecepatan frame game
clock = pygame.time.Clock()
FPS = 60


# Kelas untuk mengontrol Papan Pemukul (Striker)
class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        """Inisialisasi posisi, ukuran, kecepatan, dan warna striker."""
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color
        self.strikerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def display(self):
        """Merender striker ke layar dengan sudut agak melengkung/modern."""
        pygame.draw.rect(screen, self.color, self.strikerRect, border_radius=4)

    def update(self, xFac):
        """Memperbarui posisi striker dan membatasinya agar tidak keluar layar."""
        self.posx += self.speed * xFac
        if self.posx <= 0:
            self.posx = 0
        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width
        self.strikerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def getRect(self):
        """Mengembalikan objek Rect dari striker untuk keperluan deteksi tabrakan."""
        return self.strikerRect

