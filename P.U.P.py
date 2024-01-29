import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80  # Increase the paddle height
BALL_RADIUS = 17
FPS = 90

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Power-Up Pong")

# Load background music
pygame.mixer.music.load("PUP.mp3")  # Replace with your music file
pygame.mixer.music.set_volume(1)  # Set the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Loop indefinitely

# Clock to control the frame rate
clock = pygame.time.Clock()

# Initialize paddles and ball
player1_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS, BALL_RADIUS)

# Initial ball position and speed
ball_start_pos = (WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2)
ball_speed = [4, 4]

# Game states
TITLE_SCREEN = 0
COUNTDOWN = 1
PLAYING = 2
GAME_OVER = 3
PAUSED = 4  # Added PAUSED state
current_state = TITLE_SCREEN

# Load pixel-like font
font_pixel_title = pygame.font.Font("PressStart2P-Regular.ttf", 36)
font_pixel_small = pygame.font.Font("PressStart2P-Regular.ttf", 16)
font_pixel_large = pygame.font.Font("PressStart2P-Regular.ttf", 24)

# Scores
score_player1 = 0
score_player2 = 0

# Countdown variables
countdown_timer = 3
countdown_font = pygame.font.Font("PressStart2P-Regular.ttf", 40)
countdown_text = None

# Winner text
winner_font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
winner_text = None

# Pause text
pause_font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
paused_text = pause_font.render("PAUSED!", True, WHITE)
press_esc_text = pause_font.render("press ESC to exit game", True, WHITE)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_state == PLAYING:
                    current_state = PAUSED
                elif current_state == PAUSED:
                    current_state = COUNTDOWN
            elif event.key == pygame.K_ESCAPE:
                if current_state == PAUSED:
                    current_state = TITLE_SCREEN
                    # Reset game-related variables
                    score_player1 = 0
                    score_player2 = 0
                    ball.x, ball.y = ball_start_pos
                    countdown_timer = 3
                    countdown_text = None
            elif event.key == pygame.K_RETURN:
                if current_state == TITLE_SCREEN:
                    current_state = COUNTDOWN
                    # Reset game-related variables
                    score_player1 = 0
                    score_player2 = 0
                    ball.x, ball.y = ball_start_pos
                    countdown_timer = 3
                    countdown_text = None

    keys = pygame.key.get_pressed()

    if current_state == TITLE_SCREEN:
        # Display title screen
        title_pup_text = font_pixel_large.render("= P.U.P =", True, WHITE)
        title_pong_text = font_pixel_large.render("!POWER-UP PONG!", True, WHITE)
        start_text = font_pixel_small.render("press ENTER to start", True, WHITE)

        screen.fill(BLACK)
        screen.blit(title_pup_text, (WIDTH // 2 - title_pup_text.get_width() // 2, HEIGHT // 3 - title_pup_text.get_height() // 2))
        screen.blit(title_pong_text, (WIDTH // 2 - title_pong_text.get_width() // 2, HEIGHT // 2 - title_pong_text.get_height() // 2))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT * 2 // 3))

        if keys[pygame.K_RETURN]:
            current_state = COUNTDOWN
            # Reset game-related variables
            score_player1 = 0
            score_player2 = 0
            ball.x, ball.y = ball_start_pos
            countdown_timer = 3
            countdown_text = None

    elif current_state == COUNTDOWN:
        # Countdown before starting the game
        if countdown_timer > 0:
            countdown_text = countdown_font.render(str(countdown_timer), True, WHITE)
            screen.fill(BLACK)
            if countdown_text:
                screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
            pygame.display.flip()
            time.sleep(1)
            countdown_timer -= 1
        else:
            current_state = PLAYING
            countdown_text = None  # Define countdown_text when countdown is finished

    elif current_state == PLAYING:
        # Player 1 controls
        if keys[pygame.K_w] and player1_paddle.top > 0:
            player1_paddle.y -= 5
        if keys[pygame.K_s] and player1_paddle.bottom < HEIGHT:
            player1_paddle.y += 5

        # Player 2 controls
        if keys[pygame.K_UP] and player2_paddle.top > 0:
            player2_paddle.y -= 5
        if keys[pygame.K_DOWN] and player2_paddle.bottom < HEIGHT:
            player2_paddle.y += 5

        # Ball movement
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Ball collisions
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]

        if ball.colliderect(player1_paddle) or ball.colliderect(player2_paddle):
            ball_speed[0] = -ball_speed[0]

        # Ball goes out of bounds
        if ball.left <= 0:
            score_player2 += 1
            ball.x, ball.y = ball_start_pos
        elif ball.right >= WIDTH:
            score_player1 += 1
            ball.x, ball.y = ball_start_pos

        # Check for game over
        if score_player1 == 10 or score_player2 == 10:
            current_state = GAME_OVER
            winner_text = winner_font.render("Player 1 Wins!" if score_player1 == 10 else "Player 2 Wins!", True, WHITE)

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player1_paddle)
        pygame.draw.rect(screen, WHITE, player2_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Draw scores
        score_text = font_pixel_small.render(f"Player 1: {score_player1}  |  Player 2: {score_player2}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    elif current_state == PAUSED:
        screen.fill(BLACK)
        screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2 - paused_text.get_height() // 2))
        screen.blit(press_esc_text, (WIDTH // 2 - press_esc_text.get_width() // 2, HEIGHT * 3 // 4))

    elif current_state == GAME_OVER:
        screen.fill(BLACK)
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
        press_enter_text = pause_font.render("press ENTER to continue", True, WHITE)
        screen.blit(press_enter_text, (WIDTH // 2 - press_enter_text.get_width() // 2, HEIGHT * 3 // 4))

        if keys[pygame.K_RETURN]:
            current_state = COUNTDOWN
            # Reset game-related variables
            score_player1 = 0
            score_player2 = 0

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
