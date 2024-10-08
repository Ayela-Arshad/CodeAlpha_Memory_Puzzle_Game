import random

class MemoryPuzzleGame:
    def __init__(self):
        self.cards = []
        self.matched_pairs = 0
        self.total_cards = 0
        self.first_selection = None
        self.second_selection = None
        self.matched = set()  # Keep track of matched cards

    def create_deck(self, total_cards):
        """Creates a deck for a given number of total cards."""
        self.total_cards = total_cards
        self.matched_pairs = 0
        self.matched = set()

        # Ensure the total number of cards is even for pairing
        assert total_cards % 2 == 0, "Total cards should be an even number for pairing."

        # The actual card images will be loaded in the GUI, so we just set up the deck size here
        self.cards = [None] * total_cards  # Placeholder for card images, the GUI will handle actual images

    def select_card(self, index):
        """Handle card selection logic."""
        if self.first_selection is None:
            self.first_selection = index
            return None
        elif self.second_selection is None:
            self.second_selection = index
            return self.first_selection, self.second_selection

    def check_match(self, card1_index, card2_index, card_images):
        """Check if two selected cards are a match based on their images."""
        return card_images[card1_index] == card_images[card2_index]

    def process_selection(self, card_images):
        """Process the selected cards and determine if they match based on their images."""
        if self.first_selection is not None and self.second_selection is not None:
            card1_index = self.first_selection
            card2_index = self.second_selection
            self.first_selection, self.second_selection = None, None  # Reset selections

            if self.check_match(card1_index, card2_index, card_images):
                self.matched_pairs += 1
                self.matched.add(card1_index)
                self.matched.add(card2_index)
                return True
            else:
                return False
        return None

    def is_game_won(self):
        """Check if all pairs have been matched."""
        return self.matched_pairs == self.total_cards // 2

    def reset_game(self):
        """Reset the game variables."""
        self.first_selection = None
        self.second_selection = None
        self.matched_pairs = 0
        self.matched.clear()
