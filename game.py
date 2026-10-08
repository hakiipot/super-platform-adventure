import pygame
import sys

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

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 70)

# =========================
# PLAYER
# =========================
player = pygame.Rect(100, 400, 40, 50)

player_x = 100
player_y = 400

velocity_y = 0
speed = 5
gravity = 0.8
jump_power = -15

on_ground = False

# =========================
# PLATFORMS
# =========================
platforms = [
    pygame.Rect(0, 550, 1000, 50),
    pygame.Rect(150, 450, 150, 20),
    pygame.Rect(400, 380, 150, 20),
    pygame.Rect(650, 450, 150, 20),
    pygame.Rect(850, 350, 120, 20),
]

# =========================
# COINS
# =========================
coins = [
    pygame.Rect(200, 410, 20, 20),
    pygame.Rect(450, 340, 20, 20),
    pygame.Rect(700, 410, 20, 20),
    pygame.Rect(890, 310, 20, 20),
]

score = 0

# =========================
# ENEMY
# =========================
enemy = pygame.Rect(500, 500, 40, 40)
enemy_speed = 3
enemy_direction = 1

# =========================
# GOAL
# =========================
goal = pygame.Rect(920, 280, 30, 70)

# =========================
# GAME STATE
# =========================
game_over = False
win = False


# =========================
# MAIN GAME LOOP
# =========================
while True:

    clock.tick(FPS)

    # =====================
    # EVENTS
    # =====================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = jump_power

            # Restart
            if event.key == pygame.K_r:
                player_x = 100
                player_y = 400
                velocity_y = 0
                score = 0
                game_over = False
                win = False

                coins = [
                    pygame.Rect(200, 410, 20, 20),
                    pygame.Rect(450, 340, 20, 20),
                    pygame.Rect(700, 410, 20, 20),
                    pygame.Rect(890, 310, 20, 20),
                ]

    if not game_over and not win:

        # =====================
        # MOVEMENT
        # =====================
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += speed

        # Gravity
        velocity_y += gravity
        player_y += velocity_y

        # Update player rectangle
        player.x = int(player_x)
        player.y = int(player_y)

        # =====================
        # PLATFORM COLLISION
        # =====================
        on_ground = False

        for platform in platforms:

            if player.colliderect(platform):

                # Falling onto platform
                if velocity_y > 0 and player.bottom <= platform.bottom:
                    player.bottom = platform.top
                    player_y = player.y
                    velocity_y = 0
                    on_ground = True

        # =====================
        # COIN COLLECTION
        # =====================
        for coin in coins[:]:

            if player.colliderect(coin):
                coins.remove(coin)
                score += 10

        # =====================
        # ENEMY MOVEMENT
        # =====================
        enemy.x += enemy_speed * enemy_direction

        if enemy.left <= 400:
            enemy_direction = 1

        if enemy.right >= 600:
            enemy_direction = -1

        # Enemy collision
        if player.colliderect(enemy):

            # Jump on enemy
            if velocity_y > 0 and player.bottom <= enemy.top + 20:
                enemy.x = 500
                velocity_y = jump_power
                score += 20

            else:
                game_over = True

        # =====================
        # GOAL
        # =====================
        if player.colliderect(goal):
            win = True

        # =====================
        # FALLING
        # =====================
        if player.top > HEIGHT:
            game_over = True

        # Keep player on screen
        if player.left < 0:
            player.left = 0
            player_x = player.x

        if player.right > WIDTH:
            player.right = WIDTH
            player_x = player.x

    # =========================
    # DRAW BACKGROUND
    # =========================
    screen.fill(SKY)

    # Clouds
    pygame.draw.circle(screen, WHITE, (150, 100), 30)
    pygame.draw.circle(screen, WHITE, (180, 100), 40)
    pygame.draw.circle(screen, WHITE, (215, 100), 30)

    pygame.draw.circle(screen, WHITE, (700, 130), 30)
    pygame.draw.circle(screen, WHITE, (735, 130), 40)
    pygame.draw.circle(screen, WHITE, (770, 130), 30)

    # =========================
    # DRAW PLATFORMS
    # =========================
    for platform in platforms:
        pygame.draw.rect(screen, BROWN, platform)

        # Grass on top
        grass = pygame.Rect(
            platform.x,
            platform.y,
            platform.width,
            8
        )

        pygame.draw.rect(screen, GREEN, grass)

    # =========================
    # DRAW COINS
    # =========================
    for coin in coins:
        pygame.draw.circle(
            screen,
            YELLOW,
            coin.center,
            10
        )

    # =========================
    # DRAW ENEMY
    # =========================
    pygame.draw.rect(screen, RED, enemy)

    # Enemy eyes
    pygame.draw.circle(screen, WHITE, (enemy.x + 10, enemy.y + 12), 5)
    pygame.draw.circle(screen, WHITE, (enemy.x + 30, enemy.y + 12), 5)

    pygame.draw.circle(screen, BLACK, (enemy.x + 10, enemy.y + 12), 2)
    pygame.draw.circle(screen, BLACK, (enemy.x + 30, enemy.y + 12), 2)

    # =========================
    # DRAW GOAL
    # =========================
    pygame.draw.rect(screen, BLACK, (goal.x, goal.y, 5, 70))
    pygame.draw.polygon(
        screen,
        GREEN,
        [
            (goal.x + 5, goal.y),
            (goal.x + 35, goal.y + 15),
            (goal.x + 5, goal.y + 30)
        ]
    )

    # =========================
    # DRAW PLAYER
    # =========================

    # Body
    pygame.draw.rect(screen, BLUE, player)

    # Shirt
    pygame.draw.rect(
        screen,
        RED,
        (player.x, player.y, player.width, 18)
    )

    # Face
    pygame.draw.rect(
        screen,
        (255, 200, 150),
        (player.x + 7, player.y + 15, 26, 25)
    )

    # Eyes
    pygame.draw.circle(
        screen,
        BLACK,
        (player.x + 14, player.y + 25),
        3
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (player.x + 27, player.y + 25),
        3
    )

    # =========================
    # SCORE
    # =========================
    score_text = font.render(
        "Score: " + str(score),
        True,
        BLACK
    )

    screen.blit(score_text, (20, 20))

    # Controls
    controls = font.render(
        "A/D or Arrow Keys = Move   SPACE = Jump",
        True,
        BLACK
    )

    screen.blit(controls, (20, 55))

    # =========================
    # GAME OVER
    # =========================
    if game_over:

        text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        restart = font.render(
            "Press R to restart",
            True,
            BLACK
        )

        screen.blit(
            text,
            (
                WIDTH // 2 - text.get_width() // 2,
                HEIGHT // 2 - 60
            )
        )

        screen.blit(
            restart,
            (
                WIDTH // 2 - restart.get_width() // 2,
                HEIGHT // 2 + 20
            )
        )

    # =========================
    # WIN
    # =========================
    if win:

        text = big_font.render(
            "YOU WIN!",
            True,
            GREEN
        )

        restart = font.render(
            "Press R to play again",
            True,
            BLACK
        )

        screen.blit(
            text,
            (
                WIDTH // 2 - text.get_width() // 2,
                HEIGHT // 2 - 60
            )
        )

        screen.blit(
            restart,
            (
                WIDTH // 2 - restart.get_width() // 2,
                HEIGHT // 2 + 20
            )
        )

    pygame.display.update()
