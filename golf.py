import pygame as pg
import sys
import math

class Constants:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    GRAVITY = 9.8
    BOUNCE = 0.8
    FPS = 60
    GAME_SPEED = 0.016
    AIR_RESISTANCE = 0.001
    FRICTION = 0.35

class Colors:
    WHITE = (255, 255, 255)
    GREEN = (34, 139, 34)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

class Ball:
    def __init__(self, x, y, z=50, radius=10, color=Colors.RED):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.color = color

        self.vx = 0
        self.vy = 0
        self.vz = 0

        self.bounce = Constants.BOUNCE
        self.air_resistance = Constants.AIR_RESISTANCE
        self.ax = 0
        self.ay = 0
        self.friction = Constants.FRICTION

    def update(self, dt):
        air_resist_x = -self.air_resistance * self.vx
        air_resist_y = -self.air_resistance * self.vy

        self.vx += air_resist_x
        self.vy += air_resist_y

        self.vz -= Constants.GRAVITY * dt

        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

        if self.z <= 0:
            self.z = 0
            self.vz = -self.vz * self.bounce
            self.vx *= self.friction
            self.vy *= self.friction

        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx * self.bounce
        elif self.x + self.radius > Constants.SCREEN_WIDTH:
            self.x = Constants.SCREEN_WIDTH - self.radius
            self.vx = -self.vx * self.bounce

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy * self.bounce
        elif self.y + self.radius > Constants.SCREEN_HEIGHT:
            self.y = Constants.SCREEN_HEIGHT - self.radius
            self.vy = -self.vy * self.bounce

        if abs(self.vx) < 0.01:
            self.vx = 0
        if abs(self.vy) < 0.01:
            self.vy = 0

    def show(self, window):
        z_color_intensity = max(50, min(255, 255 - int(self.z)))
        display_color = (self.color[0], self.color[1], z_color_intensity)

        pg.draw.circle(window, display_color, (int(self.x), int(self.y)), self.radius)

        shadow_radius = max(1, int(self.radius * (1 - self.z / 100)))
        pg.draw.circle(window, Colors.BLACK, (int(self.x), int(self.y)), shadow_radius)

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

def main():
    pg.init()
    window = pg.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    pg.display.set_caption("Golf")
    clock = pg.time.Clock()

    ball = Ball(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2, z=0)
    hole = Hole(700, 550)

    shots = 0
    aiming = False
    aim_x, aim_y = 0, 0
    aiming_screen = True
    aiming_start_time = None

    previous_positions = []

    dragging = False
    drag_start_x, drag_start_y = 0, 0

    while True:
        dt = clock.tick(Constants.FPS) / 1000

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
                if aiming_screen:
                    aim_x, aim_y = mouse_x, mouse_y
                    aiming = True
                    aiming_screen = False
                    previous_positions = []
                elif ball.x - ball.radius < mouse_x < ball.x + ball.radius and ball.y - ball.radius < mouse_y < ball.y + ball.radius:
                    dragging = True
                    drag_start_x, drag_start_y = mouse_x, mouse_y
            elif event.type == pg.MOUSEBUTTONUP:
                if dragging:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    dx = mouse_x - ball.x
                    dy = mouse_y - ball.y
                    angle = math.atan2(dy, dx)

                    speed = math.sqrt((mouse_x - drag_start_x) ** 2 + (mouse_y - drag_start_y) ** 2) * 0.2
                    ball.vx = speed * math.cos(angle)
                    ball.vy = speed * math.sin(angle)
                    ball.vz = 20
                    shots += 1
                    dragging = False
            elif event.type == pg.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = event.pos

        if aiming_screen:
            window.fill(Colors.GREEN)
            ball.show(window)
            if aiming:
                pg.draw.circle(window, Colors.RED, (aim_x, aim_y), 5)
            font = pg.font.Font(None, 36)
            aim_text = font.render('Hedef Al', True, Colors.WHITE)
            text_rect = aim_text.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2 - 50))
            window.blit(aim_text, text_rect)
        else:
            ball.update(Constants.GAME_SPEED)
            window.fill(Colors.GREEN)

            previous_positions.append((ball.x, ball.y))

            ball.show(window)
            hole.show(window)

            if len(previous_positions) > 1:
                for i in range(len(previous_positions) - 1):
                    pg.draw.line(window, Colors.RED, previous_positions[i], previous_positions[i + 1], 2)

            if hole.check_collision(ball):
                print("Tebrikler! Deliğe girdiniz!")
                print(f"Toplam Vuruş Sayısı: {shots}")
                pg.quit()
                sys.exit()

            font = pg.font.Font(None, 36)
            score_text = font.render(f'Vuruş Sayısı: {shots}', True, Colors.WHITE)
            window.blit(score_text, (10, 10))

            speed_text = font.render(f'Hız: {math.sqrt(ball.vx**2 + ball.vy**2):.2f}', True, Colors.WHITE)
            window.blit(speed_text, (10, 50))

            if not aiming:
                pg.draw.line(window, Colors.RED, (ball.x, ball.y), (aim_x, aim_y), 2)

            if dragging:
                pg.draw.line(window, Colors.BLUE, (ball.x, ball.y), (mouse_x, mouse_y), 2)

            is_ball_stopped = (abs(ball.vx) < 0.01 and 
                             abs(ball.vy) < 0.01 and 
                             abs(ball.vz) < 0.01 and 
                             ball.z <= 0)

            if is_ball_stopped and not dragging:
                aiming_screen = True
                aiming = False
                ball.vx, ball.vy, ball.vz = 0, 0, 0
                previous_positions = []

        print(f"Topun Konumu: ({ball.x}, {ball.y}, {ball.z})")

        pg.display.flip()

if __name__ == "__main__":
    main()
