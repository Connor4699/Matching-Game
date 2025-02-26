class GameBoard: 
    
    def initialize_game_window():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Matching Game")

    # Iterating through the images folder and generates images for the matching game
    card_images = []
    for i in range(1, 9):
        img = pygame.image.load(rf"C:\Users\Admin\Downloads\CS project FPT\CS project FPT\images\card_{i}.png")
        img = pygame.transform.scale(img, (CARD_SIZE, CARD_SIZE))
        card_images.append(img)

    # Duplicate images for pairs
    card_images *= 2

    # Shuffle cards
    random.shuffle(card_images)

    return screen, card_images

def draw_top_menu(screen):
    pygame.draw.rect(screen, GREEN, (0, 0, WIDTH, 100))
    font = pygame.font.Font(None, 50)
    # Create a text surface with the title
    title_text = font.render("The Matching Game", True, WHITE)
    # Get the rectangle of the text surface
    title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
    # Draw the title on the top menu
    screen.blit(title_text, title_rect)
    # Add menu items or text if needed

def draw_bottom_menu(screen, elapsed_time, all_matches_found):
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 100, WIDTH, 100))
    # Set the font and size
    font = pygame.font.Font(None, 24)
    # Convert elapsed time to seconds
    elapsed_seconds = elapsed_time // 1000
    # Create a text surface with the timer
    if not all_matches_found:
        timer_text = font.render(f"Timer: {elapsed_seconds} seconds", True, WHITE)
        # Get the rectangle of the text surface
        timer_rect = timer_text.get_rect(center=(WIDTH // 2, HEIGHT - 25))
        # Draw the timer on the bottom menu
        screen.blit(timer_text, timer_rect)
        # Add menu items or text if needed

    # Display a message when all matches are found
    if all_matches_found:
        pygame.mixer.music.play(0)
        music("Pokemon_victory")
        win_text = font.render(f"Congratulations! Final time: {final_time // 1000} seconds", True, WHITE)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT - 75))
        screen.blit(win_text, win_rect)

def draw_game_screen(screen, cards, flipped_cards):
    screen.fill(WHITE)
    for card in cards:
        card_rect = card['rect'].move(cards_start_x, cards_start_y)
        if card['is_flipped']:
            screen.blit(card['image'], card_rect)
        else:
            pygame.draw.rect(screen, BLACK, card_rect)
            pygame.draw.rect(screen, WHITE, card['rect'].move(cards_start_x, cards_start_y), 2)

    # Draw red rectangle to indicate a match
    for card in flipped_cards:
        pygame.draw.rect(screen, RED, card['rect'].move(cards_start_x, cards_start_y), 5)
    
    draw_top_menu(screen) #draw the top menu 
    draw_bottom_menu(screen, elapsed_time, all_matches_found) #draw the bottom menu