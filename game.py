import pygame
import sys
import random

pygame.init()

# =========================
# SETTINGS
# =========================
WIDTH = 1000
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Platform Adventure")

clock = pygame.time.Clock()

# Colors
SKY = (100, 180, 255)
GREEN = (50, 180, 70)
BROWN = (150, 90, 40)
RED = (220, 50, 50)
YELLOW = (255, 220, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 80, 220)
ORANGE = (255, 140, 0)
PURPLE = (200, 50, 200)

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 70)

# =========================
# PLAYER
# =========================
player = pygame.Rect(100, 400, 40, 50)
player_x = 100.0
player_y = 400.0

velocity_y = 0
speed = 5
gravity = 0.8
jump_power = -15

on_ground = False
can_jump = True

# =========================
# LEVEL SYSTEM
# =========================
current_level = 1
max_levels = 100
score = 0


def get_level_difficulty(level):
    return min(2.0, 1.0 + (level - 1) * 0.015)


def generate_level_platforms(level):
    difficulty = get_level_difficulty(level)
    platforms = [pygame.Rect(0, 550, 1000, 50)]

    num_platforms = min(8, 3 + int(level / 15))
    spacing = 350 / difficulty

    for i in range(num_platforms):
        x = 150 + (i * spacing)
        if x > 900:
            break
        y = 500 - (i * 80)
        width = max(100, 180 - int(level * 0.5))
        platforms.append(pygame.Rect(int(x), int(y), width, 20))

    platforms.append(pygame.Rect(850, 200, 120, 20))
    return platforms


def generate_level_coins(level):
    coins = []
    num_coins = min(15, 4 + int(level / 20))
    for _ in range(num_coins):
        x = random.randint(150, 900)
        y = random.randint(100, 450)
        coins.append(pygame.Rect(x, y, 20, 20))
    return coins


def generate_level_enemies(level):
    difficulty = get_level_difficulty(level)
    enemies = []
    num_enemies = min(5, 1 + int(level / 20))

    for _ in range(num_enemies):
        x = random.randint(300, 700)
        y = 480
        speed = 2 + (difficulty * 2)
        enemies.append({
            'rect': pygame.Rect(x, y, 40, 40),
            'speed': speed,
            'direction': 1,
            'min_x': max(100, x - 150),
            'max_x': min(800, x + 150),
            'health': 1
        })

    return enemies


def create_boss(level):
    if level == 50:
        return {
            'rect': pygame.Rect(400, 200, 60, 80),
            'speed': 3,
            'direction': 1,
            'health': 3,
            'name': 'Level 50 Boss'
        }
    elif level == 100:
        return {
            'rect': pygame.Rect(400, 150, 80, 100),
            'speed': 4,
            'direction': 1,
            'health': 5,
            'name': 'Final Boss'
        }
    return None


platforms = generate_level_platforms(current_level)
coins = generate_level_coins(current_level)
enemies = generate_level_enemies(current_level)
boss = create_boss(current_level) if current_level in [50, 100] else None

goal = pygame.Rect(920, 120, 30, 70)

game_over = False
win = False
level_complete = False


def reset_level():
    global player_x, player_y, velocity_y, on_ground, can_jump, platforms, coins, enemies, boss, level_complete

    player_x = 100.0
    player_y = 400.0
    velocity_y = 0
    on_ground = False
    can_jump = True
    level_complete = False

    platforms = generate_level_platforms(current_level)
    coins = generate_level_coins(current_level)
    enemies = generate_level_enemies(current_level)
    boss = create_boss(current_level) if current_level in [50, 100] else None


while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground and can_jump:
                velocity_y = jump_power
                can_jump = False
                on_ground = False

            if event.key == pygame.K_n and level_complete:
                if current_level < max_levels:
                    current_level += 1
                    reset_level()
                    game_over = False
                    win = False

            if event.key == pygame.K_r and (game_over or (level_complete and current_level == max_levels)):
                current_level = 1
                score = 0
                reset_level()
                game_over = False
                win = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                can_jump = True

    if not game_over and not level_complete:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += speed

        velocity_y += gravity
        player_y += velocity_y

        player.x = int(player_x)
        player.y = int(player_y)

        on_ground = False
        for platform in platforms:
            if player.colliderect(platform):
                if velocity_y > 0 and player.bottom <= platform.bottom + 10:
                    player.bottom = platform.top
                    player_y = float(player.y)
                    velocity_y = 0
                    on_ground = True

        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                score += 10

        for enemy in enemies[:]:
            enemy['rect'].x += enemy['speed'] * enemy['direction']

            if enemy['rect'].left <= enemy['min_x']:
                enemy['direction'] = 1
            if enemy['rect'].right >= enemy['max_x']:
                enemy['direction'] = -1

            if player.colliderect(enemy['rect']):
                if velocity_y > 0 and player.bottom <= enemy['rect'].top + 20:
                    enemy['health'] -= 1
                    velocity_y = jump_power
                    on_ground = False
                    score += 20
                    if enemy['health'] <= 0:
                        enemies.remove(enemy)
                else:
                    game_over = True

        if boss:
            boss['rect'].x += boss['speed'] * boss['direction']
            if boss['rect'].left <= 250:
                boss['direction'] = 1
            if boss['rect'].right >= 750:
                boss['direction'] = -1

            if player.colliderect(boss['rect']):
                if velocity_y > 0 and player.bottom <= boss['rect'].top + 20:
                    boss['health'] -= 1
                    velocity_y = jump_power
                    on_ground = False
                    score += 50
                    if boss['health'] <= 0:
                        level_complete = True
                        win = True
                else:
                    game_over = True

        if not boss and player.colliderect(goal):
            level_complete = True
            win = True

        if player.top > HEIGHT:
            game_over = True

        if player.left < 0:
            player.left = 0
            player_x = float(player.x)

        if player.right > WIDTH:
            player.right = WIDTH
            player_x = float(player.x)

    screen.fill(SKY)

    pygame.draw.circle(screen, WHITE, (150, 100), 30)
    pygame.draw.circle(screen, WHITE, (180, 100), 40)
    pygame.draw.circle(screen, WHITE, (215, 100), 30)
    pygame.draw.circle(screen, WHITE, (700, 130), 30)
    pygame.draw.circle(screen, WHITE, (735, 130), 40)
    pygame.draw.circle(screen, WHITE, (770, 130), 30)

    for platform in platforms:
        pygame.draw.rect(screen, BROWN, platform)
        grass = pygame.Rect(platform.x, platform.y, platform.width, 8)
        pygame.draw.rect(screen, GREEN, grass)

    for coin in coins:
        pygame.draw.circle(screen, YELLOW, coin.center, 10)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy['rect'])
        pygame.draw.circle(screen, WHITE, (enemy['rect'].x + 10, enemy['rect'].y + 12), 5)
        pygame.draw.circle(screen, WHITE, (enemy['rect'].x + 30, enemy['rect'].y + 12), 5)
        pygame.draw.circle(screen, BLACK, (enemy['rect'].x + 10, enemy['rect'].y + 12), 2)
        pygame.draw.circle(screen, BLACK, (enemy['rect'].x + 30, enemy['rect'].y + 12), 2)

    if boss:
        boss_color = PURPLE if current_level == 50 else ORANGE
        pygame.draw.rect(screen, boss_color, boss['rect'])
        pygame.draw.circle(screen, WHITE, (boss['rect'].x + 15, boss['rect'].y + 20), 7)
        pygame.draw.circle(screen, WHITE, (boss['rect'].x + 45, boss['rect'].y + 20), 7)
        pygame.draw.circle(screen, BLACK, (boss['rect'].x + 15, boss['rect'].y + 20), 3)
        pygame.draw.circle(screen, BLACK, (boss['rect'].x + 45, boss['rect'].y + 20), 3)

        health_bar_width = 150
        health_bar_height = 15
        health_bar_x = boss['rect'].centerx - health_bar_width // 2
        health_bar_y = boss['rect'].top - 25
        pygame.draw.rect(screen, RED, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        max_health = 3 if current_level == 50 else 5
        health_fill = (boss['health'] / max_health) * health_bar_width
        pygame.draw.rect(screen, GREEN, (health_bar_x, health_bar_y, health_fill, health_bar_height))
        pygame.draw.rect(screen, BLACK, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)

    if not boss:
        pygame.draw.rect(screen, BLACK, (goal.x, goal.y, 5, 70))
        pygame.draw.polygon(screen, GREEN, [(goal.x + 5, goal.y), (goal.x + 35, goal.y + 15), (goal.x + 5, goal.y + 30)])

    pygame.draw.rect(screen, BLUE, player)
    pygame.draw.rect(screen, RED, (player.x, player.y, player.width, 18))
    pygame.draw.rect(screen, (255, 200, 150), (player.x + 7, player.y + 15, 26, 25))
    pygame.draw.circle(screen, BLACK, (player.x + 14, player.y + 25), 3)
    pygame.draw.circle(screen, BLACK, (player.x + 27, player.y + 25), 3)

    level_text = font.render(f"Level: {current_level}/{max_levels}", True, BLACK)
    screen.blit(level_text, (WIDTH - 250, 20))

    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (20, 20))

    controls = font.render("A/D or Arrow Keys = Move   SPACE = Jump", True, BLACK)
    screen.blit(controls, (20, 55))

    if game_over:
        text = big_font.render("GAME OVER", True, RED)
        restart = font.render("Press R to restart from Level 1", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 20))

    if level_complete and win:
        if current_level == max_levels:
            text = big_font.render("YOU WIN!", True, GREEN)
            sub_text = font.render(f"Final Score: {score}", True, BLACK)
            restart = font.render("Press R to play again from Level 1", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 80))
            screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 - 10))
            screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 40))
        else:
            text = font.render(f"LEVEL {current_level} COMPLETE!", True, GREEN)
            next_level = font.render(f"Score: {score}   Press N for next level", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(next_level, (WIDTH // 2 - next_level.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.update()
