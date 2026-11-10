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


# Kelas untuk mengontrol Blok/Bata
class Block:
    def __init__(self, posx, posy, width, height, color):
        """Inisialisasi posisi, ukuran, warna, dan health (nyawa) blok."""
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100

        if color == RED:
            self.health = 300
        elif color == WHITE:
            self.health = 200
        else:
            self.health = 100

        self.blockRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def display(self):
        """Menampilkan blok dengan efek border tipis agar terlihat seperti balok neon."""
        if self.health > 0:
            current_color = self.color
            if self.health == 200 and self.color == RED:
                current_color = WHITE
            elif self.health == 100 and (self.color == RED or self.color == WHITE):
                current_color = GREEN
            
            # Menggambar isi balok dan garis pinggirnya agar berkesan estetik
            pygame.draw.rect(screen, current_color, self.blockRect, border_radius=3)
            pygame.draw.rect(screen, BLACK, self.blockRect, 2, border_radius=3)

    def hit(self):
        """Mengurangi health blok ketika terkena bola."""
        self.health -= self.damage

    def getRect(self):
        """Mengembalikan objek Rect dari blok."""
        return self.blockRect

    def getHealth(self):
        """Mengembalikan nilai health saat ini dari blok."""
        return self.health


# Kelas untuk mengontrol Bola dengan Efek Jejak (Trail)
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        """Inisialisasi posisi, radius, kecepatan, dan riwayat jejak bola."""
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 0, 0
        self.is_moving = False
        self.trail = []  # Menyimpan riwayat posisi untuk efek visual jejak (motion blur)

        self.ball = pygame.draw.circle(
            screen, self.color, (int(self.posx), int(self.posy)), self.radius)

    def display(self):
        """Menampilkan efek jejak bola (trail) dan bola utamanya ke layar."""
        # Render efek jejak (lingkaran transparan/mengecil di belakang bola)
        for pos in self.trail:
            pygame.draw.circle(screen, (50, 50, 80), (int(pos[0]), int(pos[1])), self.radius - 2)

        # Render bola utama
        self.ball = pygame.draw.circle(
            screen, self.color, (int(self.posx), int(self.posy)), self.radius)

    def update(self, striker=None):
        """Memperbarui koordinat bola serta menyimpan riwayat posisi untuk efek jejak."""
        if not self.is_moving and striker is not None:
            self.posx = striker.posx + striker.width // 2
            self.posy = striker.posy - self.radius
            self.trail.clear()
        else:
            # Simpan posisi saat ini ke dalam list trail sebelum bergerak
            self.trail.append((self.posx, self.posy))
            if len(self.trail) > 6:  # Batasi panjang jejak
                self.trail.pop(0)

            self.posx += self.xFac * self.speed
            self.posy += self.yFac * self.speed

            if self.posx <= 0 or self.posx >= WIDTH:
                self.xFac *= -1

            if self.posy <= 0:
                self.yFac *= -1

            if self.posy >= HEIGHT:
                return True

        return False

    def launch(self):
        """Meluncurkan bola dari posisi striker ke atas."""
        if not self.is_moving:
            self.is_moving = True
            self.xFac = random.choice([-1, 1])
            self.yFac = -1

    def hit(self):
        """Membalikkan arah sumbu Y bola saat terjadi tabrakan."""
        self.yFac *= -1

    def getRect(self):
        """Mengembalikan objek Rect pembatas lingkaran bola."""
        return self.ball


# Kelas untuk Item Power-Up yang Jatuh (Multi-Ball, Wide Paddle, Extra Life)
class PowerUp:
    def __init__(self, posx, posy):
        """Inisialisasi jenis power-up secara acak (Kuning: Bola, Cyan: Papan Lebar, Ungu: Nyawa)."""
        self.width, self.height = 24, 24
        self.posx = posx
        self.posy = posy
        self.speed = 2.5
        
        # Menentukan jenis power-up secara probabilitas
        choice_val = random.random()
        if choice_val < 0.5:
            self.type = 'BALL'
            self.color = YELLOW
        elif choice_val < 0.8:
            self.type = 'WIDE'
            self.color = CYAN
        else:
            self.type = 'LIFE'
            self.color = PURPLE

        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def display(self):
        """Merender item power-up dengan ikon huruf di dalamnya agar informatif."""
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=5)
        
        # Menampilkan huruf inisial di dalam kotak power-up
        letter_map = {'BALL': 'B', 'WIDE': 'W', 'LIFE': '+'}
        txt = font.render(letter_map[self.type], True, BLACK)
        screen.blit(txt, (self.posx + 7, self.posy + 2))

    def update(self):
        """Membuat item jatuh perlahan ke bawah."""
        self.posy += self.speed
        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def getRect(self):
        """Mengembalikan objek Rect power-up."""
        return self.rect

