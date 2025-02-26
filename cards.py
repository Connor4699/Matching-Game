class Cards:
    def create_cards(card_images):
        cards = []

        for row in range(ROWS):
            for col in range(COLS):
                index = row * COLS + col
                card = {
                    'image': card_images[index],
                    'rect': pygame.Rect(col * CARD_SIZE, row * CARD_SIZE, CARD_SIZE, CARD_SIZE),
                    'is_flipped': False,
                }
                cards.append(card)

        return cards