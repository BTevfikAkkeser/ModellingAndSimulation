import pygame as pg
import math
import sys

class Constants:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    GRAVITY = 5
    GAME_SPEED = 0.064
    X_BOUNDS_BARRIER = 10
    Y_BOUNDS_BARRIER = 10
    FPS = 60
    AIR_RESISTANCE = 0.01
    BOUNCE = 0.8

class Colors:
    WHITE = (255, 255, 255)
    GREEN = (34, 139, 34)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    SMOKE = (192, 192, 192)
    BLUE = (30, 144, 255)

class Ball:
    def __init__(self, x, y, dx=0, dy=0, radius=10, color=Colors.SMOKE, outlinecolor=Colors.RED):
        self.color = color
        self.outlinecolor = outlinecolor
        self.x = x
        self.y = y
        self.vx = dx
        self.vy = dy
        self.ax = 0
        self.ay = Constants.GRAVITY
        self.dt = Constants.GAME_SPEED
        self.radius = radius
        self.bounce = Constants.BOUNCE
        self.air_resistance = Constants.AIR_RESISTANCE

    def show(self, window):
        pg.draw.circle(window, self.outlinecolor, (int(self.x), int(self.y)), self.radius)
        pg.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius - 3)

    def update(self):
        air_resist_x = -self.air_resistance * self.vx
        air_resist_y = -self.air_resistance * self.vy

        self.vx += air_resist_x
        self.vy += air_resist_y

        self.vy += Constants.GRAVITY

        self.vx += self.ax * self.dt
        self.vy += self.ay * self.dt
        self.x += self.vx * self.dt
        self.y += self.vy * self.dt

        if self.y + self.radius > Constants.SCREEN_HEIGHT:
            self.y = Constants.SCREEN_HEIGHT - self.radius
            self.vy = -self.vy * self.bounce
            self.vx *= self.bounce

        if self.x - self.radius < 0 or self.x + self.radius > Constants.SCREEN_WIDTH:
            self.x = Constants.SCREEN_WIDTH - self.radius
            self.vx = -self.vx * self.bounce

class Hole:
    def __init__(self, x, y, radius=15):
        self.x = x
        self.y = y
        self.radius = radius

    def show(self, window):
        pg.draw.circle(window, Colors.BLACK, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, ball):
        distance = math.sqrt((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2)
        return distance <= self.radius

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)

    def show(self, window):
        pg.draw.rect(window, Colors.BLACK, self.rect)

    def check_collision(self, ball):
        if self.rect.colliderect((ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)):
            ball.vx = -ball.vx * Constants.BOUNCE
            ball.vy = -ball.vy * Constants.BOUNCE

def main():
    pg.init()
    window = pg.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    pg.display.set_caption("Golf")
    clock = pg.time.Clock()

    font = pg.font.Font(None, 36)

    levels = [
        {"hole_x": 700, "hole_y": 550, "obstacles": [Obstacle(400, 400, 100, 20)]},
        {"hole_x": 400, "hole_y": 300, "obstacles": [Obstacle(300, 200, 50, 200), Obstacle(500, 400, 100, 20)]},
        {"hole_x": 100, "hole_y": 100, "obstacles": []},
    ]
    current_level = 0

    ball = Ball(200, Constants.SCREEN_HEIGHT - 50)
    hole = Hole(levels[current_level]["hole_x"], levels[current_level]["hole_y"])
    obstacles = levels[current_level]["obstacles"]

    shooting = False
    mouse_start = (0, 0)
    shots = 0
    start_time = pg.time.get_ticks()
    time_limit = 60000  # 60 saniye süre

    while True:
        window.fill(Colors.GREEN)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN and not shooting:
                mouse_start = pg.mouse.get_pos()
                shooting = True

            elif event.type == pg.MOUSEBUTTONUP and shooting:
                mouse_end = pg.mouse.get_pos()
                dx = (mouse_start[0] - mouse_end[0]) * 2
                dy = (mouse_start[1] - mouse_end[1]) * 2
                ball.vx = dx
                ball.vy = dy
                shots += 1
                shooting = False

        ball.update()
        ball.show(window)
        hole.show(window)

        # Engelleri göster ve kontrol et
        for obs in obstacles:
            obs.show(window)
            obs.check_collision(ball)

        # Seviye tamamlanınca ilerle
        if hole.check_collision(ball):
            current_level += 1
            if current_level >= len(levels):
                print("Tebrikler! Tüm seviyeleri tamamladınız!")
                pg.quit()
                sys.exit()
            else:
                hole = Hole(levels[current_level]["hole_x"], levels[current_level]["hole_y"])
                obstacles = levels[current_level]["obstacles"]
                ball = Ball(200, Constants.SCREEN_HEIGHT - 50)
                start_time = pg.time.get_ticks()
                shots = 0

        # Zaman kontrolü
        elapsed_time = pg.time.get_ticks() - start_time
        remaining_time = max(0, (time_limit - elapsed_time) // 1000)
        if elapsed_time > time_limit:
            print("Süre doldu! Oyunu kaybettiniz!")
            pg.quit()
            sys.exit()

        # Skor ve zaman göstergesi
        score_text = font.render(f'Vuruş Sayısı: {shots}', True, Colors.WHITE)
        timer_text = font.render(f'Süre: {remaining_time}', True, Colors.WHITE)
        window.blit(score_text, (10, 10))
        window.blit(timer_text, (Constants.SCREEN_WIDTH - 150, 10))

        if shooting:
            mouse_current = pg.mouse.get_pos()
            pg.draw.circle(window, Colors.BLUE, mouse_start, 8)
            pg.draw.line(window, Colors.RED, mouse_start, mouse_current, 2)

        pg.display.flip()
        clock.tick(Constants.FPS)

if __name__ == "__main__":
    main()
