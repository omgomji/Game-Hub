import pygame
import random

def play_snake():
    # Initialize Pygame
    pygame.init()

    # Get system display info
    infoObject = pygame.display.Info()
    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h

    CELL_SIZE = 20

    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)

    # Game speed levels
    speed_levels = {
        "Slow": 5,
        "Normal": 10,
        "Fast": 15,
        "Very Fast": 20
    }

    # Create the game window
    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()

    # Load high scores from a file
    def load_high_scores():
        try:
            with open("high_scores.txt", "r") as file:
                return eval(file.read())
        except FileNotFoundError:
            return {level: 0 for level in speed_levels.keys()}

    # Save high scores to a file
    def save_high_scores(high_scores):
        with open("high_scores.txt", "w") as file:
            file.write(str(high_scores))

    # Function to display score and high score
    def display_scores():
        current_score_text = small_font.render(f"Score: {score}", True, WHITE)
        high_score_text = small_font.render(f"High Score: {high_scores[level]}", True, WHITE)
        window.blit(current_score_text, (10, 10))
        window.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

    # Function to display game over screen
    def display_game_over():
        game_over_text = font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        game_over_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        game_over_surface.fill((0, 0, 0, 128))  # Transparent black surface
        game_over_surface.blit(game_over_text, game_over_rect)

        final_score_text = small_font.render(f"Score: {score}", True, WHITE)
        final_high_score_text = small_font.render(f"High Score: {high_scores[level]}", True, WHITE)
        game_over_surface.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, game_over_rect.bottom + 20))
        game_over_surface.blit(final_high_score_text, (WIDTH // 2 - final_high_score_text.get_width() // 2, final_score_text.get_height() + final_score_text.get_height() + 10 + game_over_rect.bottom + 20))

        restart_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 70, 100, 40)
        pygame.draw.rect(game_over_surface, GREEN, restart_button_rect)
        restart_text = small_font.render("New Game", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        game_over_surface.blit(restart_text, restart_text_rect)

        return game_over_surface, restart_button_rect

    # Function to display level selector GUI
    def display_level_selector():
        text = font.render("Select Game Speed:", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        window.blit(text, text_rect)

        button_width, button_height = 200, 50
        button_x = WIDTH // 2 - button_width // 2
        button_y = HEIGHT // 2 + 20

        buttons = []
        for idx, (level, speed) in enumerate(speed_levels.items()):
            button_rect = pygame.Rect(button_x, button_y + idx * (button_height + 10), button_width, button_height)
            pygame.draw.rect(window, GREEN, button_rect)
            button_text = small_font.render(level, True, WHITE)
            text_rect = button_text.get_rect(center=button_rect.center)
            window.blit(button_text, text_rect)
            buttons.append((button_rect, level, speed))

        return buttons

    high_scores = load_high_scores()
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 18)

    # Game variables
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = 'RIGHT'
    food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
    score = 0
    game_over = False
    game_running = False  # Initial game state not running
    game_paused = False  # Variable to track if the game is paused
    game_over_timer = 0  # Variable to track game over screen time
    game_speed = 10  # Default game speed
    level = None  # Current level

    # Display level selector at the start
    level_buttons = display_level_selector()

    while not game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = True  # End level selection and start the game
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                # Check for level selector button clicks
                for button_rect, sel_level, speed in level_buttons:
                    if button_rect.collidepoint(event.pos):
                        level = sel_level
                        game_speed = speed
                        game_running = True  # Start the game after selecting the level
                        break

        pygame.display.update()

    while game_running:
        window.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                if game_over:
                    game_over_surface, restart_button_rect = display_game_over()
                    if restart_button_rect.collidepoint(event.pos):
                        game_over = False
                        snake = [(WIDTH // 2, HEIGHT // 2)]
                        direction = 'RIGHT'
                        food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                                random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
                        score = 0
                        game_paused = False
                        game_over_timer = 0

        if not game_paused:  # Only update game logic if the game is not paused
            x, y = snake[0]
            if direction == 'UP':
                y -= CELL_SIZE
            elif direction == 'DOWN':
                y += CELL_SIZE
            elif direction == 'LEFT':
                x -= CELL_SIZE
            elif direction == 'RIGHT':
                x += CELL_SIZE

            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or (x, y) in snake[1:]:
                game_over = True
                game_over_timer = pygame.time.get_ticks()  # Start the timer when game over
                game_paused = True  # Pause the game when game over

            if (x, y) == food:
                score += 1
                snake.append((x, y))
                food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                        random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

            snake = [(x, y)] + snake[:-1]

            for segment in snake:
                pygame.draw.rect(window, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

            pygame.draw.rect(window, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

            display_scores()

        if game_over:
            if score > high_scores[level]:
                high_scores[level] = score  # Update high score if the current score is higher
            game_over_surface, restart_button_rect = display_game_over()
            window.blit(game_over_surface, (0, 0))  # Display game-over surface

        pygame.display.update()
        clock.tick(game_speed)

    save_high_scores(high_scores)
    pygame.quit()
