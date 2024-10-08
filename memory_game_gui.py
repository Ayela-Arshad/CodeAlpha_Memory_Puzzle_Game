import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import time
from memory_game import MemoryPuzzleGame


class MemoryPuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Puzzle Game")

        # Full-screen mode
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Game logic instance
        self.game = MemoryPuzzleGame()

        # Timer and control variables
        self.start_time = None
        self.time_limit = 0
        self.buttons = []
        self.card_images = []  # To hold card images
        self.matched = set()

        # Load card back image
        self.card_back_image = Image.open('cards/card_back.png')
        self.card_back_image = ImageTk.PhotoImage(self.card_back_image.resize((60, 90), Image.Resampling.LANCZOS))

        # Track card selections
        self.first_card = None
        self.second_card = None
        self.is_comparing = False  # Prevent further card clicks during comparison

        # UI colors and styles
        self.bg_color = "#2c3e50"  # Dark blue-gray background
        self.button_bg = "#34495e"  # Darker blue-gray for buttons
        self.button_fg = "#ecf0f1"  # Off-white text color
        self.accent_color = "#1abc9c"  # Teal accent color
        self.secondary_accent_color = "#9b59b6"  # Soft purple accent color
        self.text_color = "#ecf0f1"  # Light gray text for contrast

        # Apply background to the root window
        self.root.configure(bg=self.bg_color)

        # UI setup
        self.level_selection_screen()

    def exit_fullscreen(self, event=None):
        """Exit full-screen mode when the Escape key is pressed."""
        self.root.attributes("-fullscreen", False)

    def load_images(self, total_cards):
        """Load playing card images and ensure we have enough pairs for the total cards."""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        images = []

        # Load images from the folder and resize them based on total cards
        for suit in suits:
            for rank in ranks:
                image_path = f'cards/{rank}_of_{suit}.png'
                img = Image.open(image_path)

                if total_cards == 50:  # Level 1: Standard size
                    img = img.resize((60, 90), Image.Resampling.LANCZOS)
                elif total_cards == 100:  # Level 2: Slightly smaller size
                    img = img.resize((50, 75), Image.Resampling.LANCZOS)
                elif total_cards == 160:  # Level 3: Smaller size to fit 160 cards
                    img = img.resize((45, 68), Image.Resampling.LANCZOS)

                images.append(ImageTk.PhotoImage(img))

        # If there are not enough unique images, reuse them to meet the required card pairs
        pairs_needed = total_cards // 2
        images_needed = images[:pairs_needed]  # Get enough images for the required pairs
        while len(images_needed) < pairs_needed:  # Reuse images if necessary
            images_needed += images[:(pairs_needed - len(images_needed))]  # Reuse from the beginning

        self.card_images = images_needed * 2  # Duplicate each image to create pairs
        random.shuffle(self.card_images)  # Shuffle the card images

    def level_selection_screen(self):
        """Display level selection screen to choose game difficulty."""
        self.level_frame = tk.Frame(self.root, bg=self.bg_color)
        self.level_frame.pack(pady=50)

        level_label = tk.Label(self.level_frame, text="Choose a level to start:", font=("Helvetica", 16), bg=self.bg_color, fg=self.accent_color)
        level_label.pack(pady=10)

        level1_button = tk.Button(self.level_frame, text="Level 1 (50 cards, 5 minutes)", command=lambda: self.start_game(50, 5 * 60),
                                  bg=self.button_bg, fg=self.button_fg, font=("Helvetica", 14), activebackground=self.secondary_accent_color)
        level1_button.pack(pady=5)

        level2_button = tk.Button(self.level_frame, text="Level 2 (100 cards, 10 minutes)", command=lambda: self.start_game(100, 10 * 60),
                                  bg=self.button_bg, fg=self.button_fg, font=("Helvetica", 14), activebackground=self.secondary_accent_color)
        level2_button.pack(pady=5)

        level3_button = tk.Button(self.level_frame, text="Level 3 (160 cards, 15 minutes)", command=lambda: self.start_game(160, 15 * 60),
                                  bg=self.button_bg, fg=self.button_fg, font=("Helvetica", 14), activebackground=self.secondary_accent_color)
        level3_button.pack(pady=5)

    def start_game(self, total_cards, time_limit):
        """Start the game based on selected level."""
        self.time_limit = time_limit

        # Remove the level selection screen
        self.level_frame.pack_forget()

        # Initialize game logic
        self.game.create_deck(total_cards)
        self.matched = set()  # Reset matched cards
        self.load_images(total_cards)  # Load the card images
        self.create_ui(total_cards)

        # Start the game timer
        self.start_time = time.time()
        self.update_timer()

    def create_ui(self, total_cards):
        """Create the game board and UI elements."""
        self.board_frame = tk.Frame(self.root, bg=self.bg_color)
        self.board_frame.pack(pady=20)

        self.buttons = []

        # Adjust the number of columns based on the level and card size
        if total_cards == 50:  # Level 1
            grid_columns = 10
        elif total_cards == 100:  # Level 2
            grid_columns = 15
        elif total_cards == 160:  # Level 3
            grid_columns = 20  # 20 cards per row for Level 3

        for i in range(self.game.total_cards):
            if total_cards == 50:
                btn = tk.Button(self.board_frame, image=self.card_back_image, width=70, height=100,
                                bg=self.button_bg, activebackground=self.accent_color, command=lambda i=i: self.reveal_card(i))
            elif total_cards == 100:
                btn = tk.Button(self.board_frame, image=self.card_back_image, width=50, height=75,
                                bg=self.button_bg, activebackground=self.accent_color, command=lambda i=i: self.reveal_card(i))
            elif total_cards == 160:
                btn = tk.Button(self.board_frame, image=self.card_back_image, width=45, height=68,  # Adjust size for visibility
                                bg=self.button_bg, activebackground=self.accent_color, command=lambda i=i: self.reveal_card(i))

            btn.grid(row=i // grid_columns, column=i % grid_columns, padx=3, pady=3)
            self.buttons.append(btn)

        self.timer_label = tk.Label(self.root, text="Time left: 5:00", font=("Helvetica", 14), bg=self.bg_color, fg=self.accent_color)
        self.timer_label.pack(pady=10)

        self.reset_button = tk.Button(self.root, text="Reset Game", command=self.reset_game, bg=self.secondary_accent_color, fg=self.button_fg, font=("Helvetica", 14), activebackground=self.accent_color)
        self.reset_button.pack(pady=10)

    def reveal_card(self, index):
        """Reveal the selected card and handle matching logic."""
        if self.is_comparing:  # Prevent further clicks during comparison
            return

        # Ignore clicks on already matched cards or same card clicked twice
        if index in self.matched or self.first_card == index:
            return

        # Reveal the card
        self.buttons[index].config(image=self.card_images[index])

        # Handle card selection logic
        if self.first_card is None:
            self.first_card = index
        elif self.second_card is None:
            self.second_card = index
            self.is_comparing = True  # Set the comparison state
            # Process match after delay to allow user to see second card
            self.root.after(1000, self.check_match)

    def check_match(self):
        """Check if the two selected cards match."""
        if self.card_images[self.first_card] == self.card_images[self.second_card]:
            # Cards match, mark them as matched
            self.matched.add(self.first_card)
            self.matched.add(self.second_card)
            if len(self.matched) == self.game.total_cards:
                tk.messagebox.showinfo("Congratulations!", "You've won the game!")
                self.reset_game()
        else:
            # Cards do not match, flip them back
            self.buttons[self.first_card].config(image=self.card_back_image)
            self.buttons[self.second_card].config(image=self.card_back_image)

        # Reset selections and comparison state
        self.first_card = None
        self.second_card = None
        self.is_comparing = False  # Allow new comparisons

    def update_timer(self):
        """Update the timer label."""
        elapsed_time = time.time() - self.start_time
        remaining_time = self.time_limit - int(elapsed_time)

        if remaining_time <= 0:
            self.timer_label.config(text="Time's up!")
            tk.messagebox.showinfo("Time's Up!", "You ran out of time!")
            self.reset_game()
        else:
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            self.timer_label.config(text=f"Time left: {minutes}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

    def reset_game(self):
        """Reset the game board and variables."""
        self.board_frame.pack_forget()
        self.timer_label.pack_forget()
        self.reset_button.pack_forget()

        self.level_selection_screen()  # Go back to level selection screen


if __name__ == "__main__":
    root = tk.Tk()
    game_gui = MemoryPuzzleGUI(root)
    root.mainloop()
