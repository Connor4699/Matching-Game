import pygame
import random
import sys
#import GameBoard

pygame.init()
pygame.mixer.init()

class Music:
    def __init__(self):
        pygame.mixer.init()

    def play_music(self, music_name):
        pygame.mixer.music.load(f"{music_name}.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=750)

    def play_sound(self, sound_name):
        sound = pygame.mixer.Sound(f"{sound_name}.mp3")
        sound.play()

    def reset_button(self):
        button_surface = pygame.Surface((100, 50))

        pygame.draw.rect(button_surface, (0, 0, 0), (0, 0, 100, 50))
        pygame.draw.rect(button_surface, (255, 255, 255), (1, 1, 98, 48))
        pygame.draw.rect(button_surface, (0, 0, 0), (1, 1, 98, 1), 2)
        pygame.draw.rect(button_surface, (0, 0, 0), (1, 48, 98, 1), 2)
        pygame.draw.text(button_surface, "Reset", (25, 25), (255, 255, 255))
        button_rect = pygame.Rect(0, 0, 100, 50)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button_rect.collidepoint(event.pos):
            self.stop_music()
            game_board = GameBoard(400, 600, 4, 4, 100)
            start_time = pygame.time.get_ticks()
            self.play_music("Theme 2")

class Card:
    def __init__(self, game_board, image, rect):
        self.game_board = game_board
        self.image = image
        self.rect = rect
        self.is_flipped = False

    @staticmethod
    def generate_card_images(card_size):
        card_images = []
        for i in range(3, 11):
            img = pygame.image.load(f"card_{i}.jpeg")
            img = pygame.transform.scale(img, (card_size, card_size))
            card_images.append(img)

        card_images *= 2  # Duplicate images for pairs
        random.shuffle(card_images)  # Shuffle cards

        return card_images

    @classmethod
    def create_cards(cls, game_board):
        card_images = cls.generate_card_images(game_board.card_size)
        cards = []

        for row in range(game_board.rows):
            for col in range(game_board.cols):
                index = row * game_board.cols + col
                card = cls(
                    game_board=game_board,
                    image=card_images[index],
                    rect=pygame.Rect(col * game_board.card_size, row * game_board.card_size, game_board.card_size,
                                     game_board.card_size),
                )
                cards.append(card)

        return cards

    def flip(self):
        if not self.is_flipped:
            self.is_flipped = True
            self.game_board.flipped_cards.append(self)

            if len(self.game_board.flipped_cards) == 2:
                if self.game_board.flipped_cards[0].image == self.game_board.flipped_cards[1].image:
                    self.game_board.flipped_cards = []

                    if all(card.is_flipped for card in self.game_board.cards):
                        self.game_board.all_matches_found = True
                        self.game_board.final_time = pygame.time.get_ticks() - self.game_board.start_time
                        
                else:
                    self.game_board.delay_timer = 15

class GameBoard:
    def __init__(self, width, height, rows, cols, card_size):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.card_size = card_size

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (34, 139, 34)

        # Global variables for card positions
        self.cards_start_x = (self.width - self.cols * self.card_size) // 2
        self.cards_start_y = (self.height - self.rows * self.card_size - 100) // 2 + 50  # Subtracting 100 for top and bottom menus
        self.font = pygame.font.Font(None, 24)
        self.victory_sound = Music()
        self.final_time = 0

        self.flipped_cards = []  # Track flipped cards
        self.delay_timer = 0  # Delay timer
        self.all_matches_found = False
        self.cards = []
        self.start_time = pygame.time.get_ticks()

    def initialize_game_window(self):
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Matching Game")

        self.cards = Card.create_cards(self)
        return screen

    def draw_top_menu(self, screen):
        pygame.draw.rect(screen, self.GREEN, (0, 0, self.width, 98))
        font = pygame.font.Font(None, 50)
        title_text = font.render("Pokemon Matching", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.width // 2, 50))
        screen.blit(title_text, title_rect)

    def draw_bottom_menu(self, screen, elapsed_time):
        pygame.draw.rect(screen, self.GREEN, (0, self.height - 98, self.width, 100))
        font = pygame.font.Font(None, 24)
        elapsed_seconds = elapsed_time // 1000

        if not self.all_matches_found:
            timer_text = font.render(f"Timer: {elapsed_seconds} seconds", True, self.WHITE)
            timer_rect = timer_text.get_rect(center=(self.width // 2, self.height - 25))
            screen.blit(timer_text, timer_rect)

        if self.all_matches_found:
            pygame.mixer.music.stop()
            # self.victory_sound.play_sound("Victory 3") # loops!
            win_text = font.render(f"Congratulations! Final time: {self.final_time // 1000} seconds", True,
                                   self.WHITE)
            win_rect = win_text.get_rect(center=(self.width // 2, self.height - 75))
            screen.blit(win_text, win_rect)
            return True

    def draw_game_screen(self, screen, elapsed_time):
        screen.fill(self.WHITE)
        for card in self.cards:
            card_rect = card.rect.move(self.cards_start_x, self.cards_start_y)
            if card.is_flipped:
                screen.blit(card.image, card_rect)
            else:
                pygame.draw.rect(screen, self.BLACK, card_rect)
                pygame.draw.rect(screen, self.WHITE, card.rect.move(self.cards_start_x, self.cards_start_y), 2)
        
        for card in self.flipped_cards:
            pygame.draw.rect(screen, self.RED, card.rect.move(self.cards_start_x, self.cards_start_y), 5)

        self.draw_top_menu(screen)
        self.draw_bottom_menu(screen, elapsed_time)

    def update_delay_timer(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        elif self.delay_timer == 0 and len(self.flipped_cards) == 2:
            self.flipped_cards[0].is_flipped = False
            self.flipped_cards[1].is_flipped = False
            self.flipped_cards = []

        return self.delay_timer


# Main game loop
if __name__ == "__main__":
    game_board = GameBoard(400, 600, 4, 4, 100)
    music = Music()
    screen = game_board.initialize_game_window()  # Initialize Pygame and set up game window
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    end_game = False
    music.play_music("Theme 2")  # Play music when the game starts
    music.reset_button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_board.all_matches_found:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for card in game_board.cards:
                    card_rect = card.rect.move(game_board.cards_start_x, game_board.cards_start_y)
                    if card_rect.collidepoint(mouse_x, mouse_y) and not card.is_flipped:
                        card.flip()

            # elif event.type == pygame.MOUSEBUTTONDOWN and game_board.all_matches_found:    
            #     music.reset_button()
        game_board.delay_timer = game_board.update_delay_timer()

        pygame.display.flip()
        clock.tick(60)
        elapsed_time = pygame.time.get_ticks() - start_time
        game_board.draw_game_screen(screen, elapsed_time)
