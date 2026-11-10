import pygame
import random

pygame.init()

# Dimensi layar permainan
WIDTH, HEIGHT = 600, 500

# Definisi Palet Warna ala Neon (Estetik untuk Gamer)
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


# Fungsi Pembantu (Helper Functions)

def collisionChecker(rect, ball):
    """Fungsi untuk memeriksa tabrakan antara dua objek Rect."""
    if rect.colliderect(ball):
        return True
    return False


def populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap):
    """Fungsi untuk menyusun daftar balok dalam arena permainan."""
    listOfBlocks = []
    start_y = 60 
    for i in range(25, WIDTH - blockWidth, blockWidth + horizontalGap):
        for j in range(start_y, HEIGHT // 2 - 20, blockHeight + verticalGap):
            chosen_color = random.choice([WHITE, GREEN, RED])
            listOfBlocks.append(
                Block(i, j, blockWidth, blockHeight, chosen_color))
    return listOfBlocks


def startScreen():
    """Fungsi untuk menampilkan layar utama (Start Menu) dengan nuansa neon."""
    waiting = True
    while waiting:
        screen.fill(BLACK)
        title_text = large_font.render("NEON BLOCK BREAKER", True, CYAN)
        instruction_text = font.render("Press SPACE Bar to Launch", True, WHITE)
        controls_text = font.render("Use LEFT & RIGHT Arrows to Move", True, GREEN)
        
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
        screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 2 + 40))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
    return False


def gameOver(score):
    """Fungsi layar Game Over saat nyawa habis."""
    run_game_over = True
    while run_game_over:
        screen.fill(BLACK)
        over_text = large_font.render("GAME OVER", True, RED)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press SPACE to Restart or ESC to Quit", True, YELLOW)
        
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 10))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 30))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
    return False


def victoryScreen(score):
    """Fungsi layar kemenangan saat seluruh balok hancur."""
    run_victory = True
    while run_victory:
        screen.fill(BLACK)
        vic_text = large_font.render("VICTORY! YOU WIN!", True, GREEN)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press SPACE to Play Again or ESC to Quit", True, YELLOW)
        
        screen.blit(vic_text, (WIDTH // 2 - vic_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 10))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 30))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
    return False


# Fungsi Utama Pengelola Game (Game Manager)
def main():
    if not startScreen():
        return

    running = True
    lives = 3
    score = 0

    striker = Striker(WIDTH // 2 - 50, HEIGHT - 40, 100, 15, 8, WHITE)
    strikerXFac = 0

    balls = [Ball(striker.posx + striker.width // 2, striker.posy - 8, 8, 5, WHITE)]
    power_ups = []
    
    # Variabel timer untuk efek power-up papan lebar (Wide Paddle)
    wide_timer = 0

    blockWidth, blockHeight = 50, 18
    horizontalGap, verticalGap = 12, 12

    listOfBlocks = populateBlocks(
        blockWidth, blockHeight, horizontalGap, verticalGap)

    # Loop Utama Permainan
    while running:
        screen.fill(BLACK)

        # Menggambar garis batas atas UI agar terlihat rapi dan elegan
        pygame.draw.line(screen, (40, 40, 60), (0, 40), (WIDTH, 40), 2)

        # Menampilkan teks informasi UI di atas layar
        scoreText = font.render(f"SCORE : {score}", True, WHITE)
        livesText = font.render(f"LIVES : {lives}", True, RED)
        activeBallsText = font.render(f"BALLS : {len(balls)}", True, YELLOW)
        
        screen.blit(scoreText, (20, 12))
        screen.blit(activeBallsText, (WIDTH // 2 - 45, 12))
        screen.blit(livesText, (WIDTH - 100, 12))

        # Mengatur durasi efek papan lebar (Wide Paddle berdurasi sekitar 8 detik / 480 frame)
        if wide_timer > 0:
            wide_timer -= 1
            if wide_timer == 0:
                striker.width = 100  # Kembalikan ukuran normal

        # Cek kondisi kemenangan
        if not listOfBlocks:
            running = victoryScreen(score)
            if running:
                lives = 3
                score = 0
                striker.width = 100
                balls = [Ball(striker.posx + striker.width // 2, striker.posy - 8, 8, 5, WHITE)]
                power_ups.clear()
                listOfBlocks = populateBlocks(blockWidth, blockHeight, horizontalGap, verticalGap)
            else:
                break

        # Penanganan Event Keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1
                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1
                if event.key == pygame.K_SPACE:
                    for ball in balls:
                        ball.launch()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    strikerXFac = 0

        # Loop pembaruan bola dan deteksi tabrakan
        for ball in balls[:]:
            if collisionChecker(striker.getRect(), ball.getRect()) and ball.is_moving:
                ball.hit()
                offset = ball.posx - (striker.posx + striker.width / 2)
                ball.xFac = offset / (striker.width / 2)

            for block in listOfBlocks[:]:
                if collisionChecker(block.getRect(), ball.getRect()) and ball.is_moving:
                    ball.hit()
                    block.hit()

                    if block.getHealth() <= 0:
                        listOfBlocks.remove(block)
                        
                        if block.color == RED:
                            score += 15
                        elif block.color == WHITE:
                            score += 10
                        else:
                            score += 5

                        # Peluang 30% menjatuhkan power-up acak
                        if random.random() < 0.30:
                            new_powerup = PowerUp(block.posx + block.width // 2 - 12, block.posy)
                            power_ups.append(new_powerup)

                    break

            lifeLost = ball.update(striker)
            if lifeLost:
                balls.remove(ball)

        # Memperbarui dan memeriksa tangkapan item Power-Up
        for p in power_ups[:]:
            p.update()
            if collisionChecker(striker.getRect(), p.getRect()):
                if p.type == 'BALL':
                    extra_ball = Ball(striker.posx + striker.width // 2, striker.posy - 15, 8, 5, YELLOW)
                    extra_ball.launch()
                    balls.append(extra_ball)
                elif p.type == 'WIDE':
                    striker.width = 150  # Perlebar papan pemukul
                    wide_timer = 480     # Durasi efek aktif
                elif p.type == 'LIFE':
                    lives += 1           # Tambah nyawa pemain
                
                power_ups.remove(p)
            elif p.posy > HEIGHT:
                power_ups.remove(p)

        # Jika semua bola habis jatuh
        if len(balls) == 0:
            lives -= 1
            power_ups.clear()
            striker.width = 100
            if lives <= 0:
                running = gameOver(score)
                if running:
                    lives = 3
                    score = 0
                    balls = [Ball(striker.posx + striker.width // 2, striker.posy - 8, 8, 5, WHITE)]
                    listOfBlocks = populateBlocks(
                        blockWidth, blockHeight, horizontalGap, verticalGap)
                else:
                    break
            else:
                balls.append(Ball(striker.posx + striker.width // 2, striker.posy - 8, 8, 5, WHITE))

        striker.update(strikerXFac)

        # Render objek ke layar
        striker.display()
        for ball in balls:
            ball.display()
        for p in power_ups:
            p.display()
        for block in listOfBlocks:
            block.display()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()