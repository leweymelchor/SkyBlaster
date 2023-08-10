import pygame
import os
pygame.font.init()
pygame.mixer.init()

# ****CONSTANTS******************************************************************************************

# SCREEN
WIDTH, HEIGHT = 1280, 716
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sky Blaster")

# COLORS:
PINK = (180, 84, 236)
LIGHT_BLUE = (1, 214, 182)

# FONTS
HEALTH_FONT = pygame.font.SysFont('pixeltype', 70)
WINNER_FONT = pygame.font.SysFont('pixeltype', 120)

# SOUNDS
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Explosion-3.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Lazer-1.wav'))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Game-Over.wav'))
BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join('Assets', 'BG-music.wav'))

# FRAME-RATE
FPS = 60

# GAME SETTINGS
VEL = 7 # 5 Ship Velocity
BULLET_VEL = 12 # 7
MAX_BULLETS = 7 # 15 = infinite

# DIMENSIONS
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 50
# TEST LINES
BORDER = pygame.Rect(WIDTH//2 - 2.5, 0, 5, HEIGHT)
# HORIZONTAL = pygame.Rect(0, HEIGHT//2 - 2.5, WIDTH, 5)
# L_LINE = pygame.Rect(100, 0, 5, HEIGHT)
# R_LINE = pygame.Rect(1180, 0, 5, HEIGHT)

# EVENTS
BLUE_HIT = pygame.USEREVENT + 1
PINK_HIT = pygame.USEREVENT + 2

# ****IMAGES****

# BLUE SHIP
BLUE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'Blue-Space-Ship-Light.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
BLUE_BLAST = pygame.image.load(os.path.join('Assets', 'Blue Blast 1.png'))

# PINK SHIP
PINK_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'Pink-Space-Ship-Dark.png'))
PINK_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(PINK_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
PINK_BLAST = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'Red Blast 1.png')), 180)

# BACKGROUND
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space-bg-2.jpeg')), (WIDTH, HEIGHT))

# *******************************************************************************************************

# ALL DRAWINGS
def draw_window(pink, blue, pink_bullets, blue_bullets, pink_health, blue_health):
    WIN.blit(SPACE, (0, 0))
    # TEST LINES
    # pygame.draw.rect(WIN, LIGHT_BLUE, HORIZONTAL)
    # pygame.draw.rect(WIN, LIGHT_BLUE, BORDER)
    # pygame.draw.rect(WIN, LIGHT_BLUE, L_LINE)
    # pygame.draw.rect(WIN, LIGHT_BLUE, R_LINE)

    # Health
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health), 1, LIGHT_BLUE)
    pink_health_text = HEALTH_FONT.render("Health: " + str(pink_health), 1, PINK)
    WIN.blit(blue_health_text, (10, HEIGHT - 40))
    WIN.blit(pink_health_text, (WIDTH - pink_health_text.get_width() - 10, 15))

    # Space Ship and Position // (300, 100) Draw Coordinates (X, Y)
    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y)) # x and y are available because of pygame Rect on line 132
    WIN.blit(PINK_SPACESHIP, (pink.x, pink.y))

    for bullet in pink_bullets:
        # pygame.draw.rect(WIN, pink, bullet)
        WIN.blit(PINK_BLAST, (bullet))

    for bullet in blue_bullets:
        # pygame.draw.rect(WIN, blue, bullet)
        WIN.blit(BLUE_BLAST, (bullet))

    pygame.display.update()


def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0: # LEFT
            blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width - 16 < BORDER.x: # RIGHT
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL > 0: # UP
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT - 10: # DOWN
        blue.y += VEL

def pink_handle_movement(keys_pressed, pink):
    if keys_pressed[pygame.K_LEFT] and pink.x - VEL > BORDER.x + BORDER.width - 5: # LEFT
            pink.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and pink.x + VEL + pink.width < WIDTH + 15: # RIGHT
        pink.x += VEL
    if keys_pressed[pygame.K_UP] and pink.y - VEL > 0: # UP
        pink.y -= VEL
    if keys_pressed[pygame.K_DOWN] and pink.y + VEL + pink.height < HEIGHT - 10: # DOWN
        pink.y += VEL

def handle_bullets(blue_bullets, pink_bullets, blue, pink):
    for bullet in blue_bullets:
        bullet.x += BULLET_VEL
        if pink.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PINK_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            blue_bullets.remove(bullet)


    for bullet in pink_bullets:
        bullet.x -= BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            pink_bullets.remove(bullet)
        elif bullet.x < 0:
            pink_bullets.remove(bullet)

def draw_blue_winner(text):
    draw_text = WINNER_FONT.render(text, 1, LIGHT_BLUE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_pink_winner(text):
    draw_text = WINNER_FONT.render(text, 1, PINK)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    # Pygame Rectangles (X-pos, Y-pos, Rect-Width, Rect-Height)
    blue = pygame. Rect(85, 330, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    pink = pygame. Rect(1160, 330, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    blue_bullets = []
    pink_bullets = []

    pink_health = 10
    blue_health = 10

    clock = pygame.time.Clock()
    run = True

    BACKGROUND_MUSIC.play(-1)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # Quits the game event listener
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


                if event.key == pygame.K_LSHIFT and len (pink_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(pink.x, pink.y + pink.height//2 - 2, 10, 5)
                    pink_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == PINK_HIT:
                pink_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == BLUE_HIT:
                blue_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if blue_health <= 0:
            winner_text = "Pink Wins!"
            # winner_text = "pink Wins!"
            GAME_OVER_SOUND.play()
            BACKGROUND_MUSIC.stop()

        if pink_health <= 0:
            winner_text = "Blue Wins!"
            # winner_text = "blue Wins!"
            GAME_OVER_SOUND.play()
            BACKGROUND_MUSIC.stop()

        if winner_text == "Pink Wins!":
            draw_pink_winner(winner_text)
            break
        if winner_text == "Blue Wins!":
            draw_blue_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        # print(pink_bullets, blue_bullets)
        blue_handle_movement(keys_pressed, blue)
        pink_handle_movement(keys_pressed, pink)

        handle_bullets(blue_bullets, pink_bullets, blue, pink)

        draw_window(pink, blue, pink_bullets, blue_bullets, pink_health, blue_health)
    main()


if __name__ == "__main__":
    main()
