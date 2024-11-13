import pygame
import random

# Pygame ayarları
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("City Life Simulation")
clock = pygame.time.Clock()

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Oyun süre ve koşul ayarları
initial_game_duration = 120  # Oyun süresi: 2 dakika
win_social_threshold = 100
lose_social_threshold = -100

# Temel sınıflar
class Zone:
    def __init__(self, name, demand, capacity, color, x, y):
        self.name = name
        self.demand = demand
        self.capacity = capacity
        self.color = color
        self.x = x
        self.y = y

    def draw(self):
        capacity_ratio = min(self.capacity / 100, 1)
        pygame.draw.rect(screen, self.color, (self.x, self.y, 200, 60))
        pygame.draw.rect(screen, GREEN, (self.x, self.y + 70, 200 * capacity_ratio, 15))
        pygame.draw.rect(screen, BLACK, (self.x, self.y + 70, 200, 15), 2)

        font = pygame.font.Font(None, 28)
        text = font.render(f"{self.name} | Demand: {self.demand} | Capacity: {self.capacity}", True, BLACK)
        screen.blit(text, (self.x, self.y + 90))

    def update(self, other_demand, social_index):
        self.demand = max(0, self.demand + random.randint(-5, 5) + social_index // 10)
        self.capacity += (self.demand - self.capacity) // 10

    def invest(self, amount):
        self.capacity += amount
        self.demand += amount // 2

# Sosyal indeks hesaplama
def calculate_social_index(zones):
    total_difference = sum([z.demand - z.capacity for z in zones])
    return total_difference

# Şehir alanlarını oluştur
def initialize_game():
    return [
        Zone("Residential", demand=50, capacity=60, color=BLUE, x=150, y=150),
        Zone("Commercial", demand=70, capacity=80, color=RED, x=500, y=150),
        Zone("Industrial", demand=40, capacity=50, color=BLACK, x=850, y=150)
    ], initial_game_duration, 0, 0

# Ana döngü
running = True
zones, time_left, pollution, tax_income = initialize_game()
game_over = False
while running:
    screen.fill(WHITE)
    dt = clock.tick(30) / 1000
    time_left -= dt
    social_index = calculate_social_index(zones)
    pollution += sum(zone.capacity * 0.01 for zone in zones)
    tax_income += sum(zone.demand * 0.02 for zone in zones)

    if social_index >= win_social_threshold:
        game_over = True
        result_text = "Kazandınız!"
    elif social_index <= lose_social_threshold or time_left <= 0:
        game_over = True
        result_text = "Kaybettiniz!"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if game_over:
                    zones, time_left, pollution, tax_income = initialize_game()
                    game_over = False
                else:
                    zones[0].invest(10)
            elif event.key == pygame.K_c and not game_over:
                zones[1].invest(10)
            elif event.key == pygame.K_i and not game_over:
                zones[2].invest(10)
            elif event.key == pygame.K_t and tax_income >= 20:
                tax_income -= 20
                for zone in zones:
                    zone.capacity += 5
            elif event.key == pygame.K_p and pollution >= 10:
                pollution -= 10
                social_index += 5

    if not game_over:
        for zone in zones:
            other_demand = sum(z.demand for z in zones if z != zone)
            zone.update(other_demand, social_index)
            zone.draw()

        font = pygame.font.Font(None, 36)
        social_text = font.render(f"Social Index: {social_index}", True, BLACK)
        screen.blit(social_text, (WIDTH // 2 - 100, HEIGHT - 220))
        
        pollution_text = font.render(f"Pollution: {int(pollution)}", True, YELLOW)
        screen.blit(pollution_text, (WIDTH // 2 - 100, HEIGHT - 180))
        
        tax_text = font.render(f"Tax Income: ${int(tax_income)}", True, BLACK)
        screen.blit(tax_text, (WIDTH // 2 - 100, HEIGHT - 140))
        
        time_text = font.render(f"Time Left: {int(time_left)}", True, BLACK)
        screen.blit(time_text, (WIDTH // 2 - 100, HEIGHT - 100))

        info_text = font.render("Invest with R, C, I | Clean Pollution with P | Raise Capacity with T", True, BLACK)
        screen.blit(info_text, (WIDTH // 2 - 300, HEIGHT - 50))
    else:
        font = pygame.font.Font(None, 48)
        end_text = font.render(result_text, True, BLACK)
        screen.blit(end_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

        restart_text = font.render("Press R to Restart", True, BLACK)
        screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))

    pygame.display.flip()

pygame.quit()
