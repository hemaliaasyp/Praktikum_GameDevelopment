import pygame, sys, random

# Memulai musik
pygame.mixer.pre_init(44100, -16, 2, 512)
# Memulai pygame
pygame.init()
clock = pygame.time.Clock()

#Mengatur size dan nama untuk screen
screen_width = 720
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Mengatur warna, font, dan musik yang akan dimasukkan dalam game
bg_color = pygame.Color('#2F373F')
accent_color = (27,35,43)
basic_font = pygame.font.Font("freesansbold.ttf", 32)
plob_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")
middle_strip = pygame.Rect(screen_width/2 - 2, 0, 4, screen_height)

# Membuat main class sprite Block
class Block (pygame.sprite.Sprite):
    def __init__(self,path,x_pos,y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))

# Membuat subclass sprite Block yaitu class Player 
class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    # Fungsi yang digunakan untuk membatasi screen
    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    # Fungsi yang digunakan untuk mengupdate.
    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()

# Membuat subclass sprite Block yaitu class Ball
class Ball(Block):
    # berisi instansiasi property dalam class
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y,paddles):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x * random.choice((-1,1))
        self.speed_y = speed_y * random.choice((-1,1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    # Fungsi untuk meng-update
    def update(self):
        # Jika bola aktif maka balok akan bergerak ke atas dan ke bawah sehingga bola bertabrakan dengan balok
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        # Jika tidak maka game akan me-restart dan memulai dari awal
        else:
            self.restart_counter()

    # Fungsi yang digunakan untuk me-reset ball
    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1,1))
        self.speed_y *= random.choice((-1,1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width/2, screen_height/2)
        pygame.mixer.Sound.play(score_sound)

    # Fungsi yang digunakan untu mengatur tabrakan yang terjadi antara balok dan bola
    def collisions(self):
        # Apabila bola memantul tidak mengenai balok di sebelah kanan maka akan dimainkan plob_sound
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(plob_sound)
            self.speed_y*= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            # Digunakan untuk memutar sound
            pygame.mixer.Sound.play(plob_sound)
            
            # Digunakan untuk mengatur pergerakan balok dengan menyesuaikan pergerakan random dari bola
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    # Menampilkan countdown yang dilakukan saat awalan game
    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = basic_font.render(str(countdown_number), True, accent_color)
        time_counter_rect = time_counter.get_rect(center = (screen_width/2, screen_height/2 + 50))
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)

# Membuat subclass sprite Block yaitu class musuh
class Opponent(Block):
    # Instansiasi property dalam class musuh(opponent)
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed

    # Meng-update ball_group
    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    # Fungsi untuk membatasi pergerakan bola agar tidak melebihi size screen
    def constrain(self):
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= screen_height: self.rect.bottom = screen_height

# Membuat class Game Manager      
class GameManager:
    # Instansiasi property dalam class game manager
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    # Fungsi run_game digunakan untuk menampilkan dan meng-update paddle_group dan ball_group
    # selain itu, juga digunakan untuk reset_ball dan juga mencetak score
    def run_game(self):
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    # Fungsi reset_ball digunakan untuk me-reset kondisi bola
    # Apabila bola bergerak ke kanan dan melebihi batas maka score musuh akan bertambah 1 kemudian bola akan kembali ke posisi awal(me-reset)
    # Apabila bola bergerak ke kiri dan <= 0 maka score player akan bertambah 1 kemudian bola akan kembali ke posisi awal(me-reset)
    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    # Fungsi yang digunakan untuk menampilkan score
    def draw_score(self):
        player_score = basic_font.render(str(self.player_score), True, accent_color)
        opponent_score = basic_font.render(str(self.opponent_score), True, accent_color)

        player_score_rect = player_score.get_rect(midleft = (screen_width/2 + 40, screen_height/2))
        opponent_score_rect = opponent_score.get_rect(midright = (screen_width/2 - 40, screen_height/2))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)

# Membuat variabel player untuk instansiasi dari kelas Player yang akan menampilkan balok yang akan digunakan oleh player.
player = Player("Paddle.png", screen_width - 20, screen_height/2, 5)
# Membuat variabel opponent untuk instansiasi dari kelas Opponent yang akan menampilkan balok yang akan digunakan oleh musuh.
opponent = Opponent("Paddle.png", 20, screen_width/2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

# Membuat variabel ball untuk instansiasi dari kelas Ball guna menampilkan bola yang nanti akan digunakan dalam permainan
ball = Ball("Ball.png", screen_width/2, screen_height/2, 4, 4, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

# Membuat variabel game_manager yang digunakan untuk instansiasi dari kelas GameManager
game_manager = GameManager(ball_sprite, paddle_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement -= player.speed
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.movement += player.speed
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed

    # Mengatur warna backgroup screen
    screen.fill(bg_color)
    # Menampilkan balok
    pygame.draw.rect(screen, accent_color, middle_strip)
    # Menjalankan variabel game_manager dengan fungsi run_game()
    game_manager.run_game()
    # Untuk meng-update tampilan screen
    pygame.display.flip()
    # Memberikan waktu 120ms untuk waktu objek bergerak
    clock.tick(120)
