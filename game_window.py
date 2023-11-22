from tkinter.messagebox import showerror
from tkinter import *
from tkinter.font import *
from game import *
from options_box import OptionsBox

SMALL_FONT = (None, 20)
FONT = (None, 50)
PADX = 5
PADY = 5
BUTTON_W = 0.75 * 100
BUTTON_H = 1 * 100
SAME_BG = "blue"
SEL_FG = "red"

MENU_PADY = 30
MENU_PADX = PADX

class GameWindow(Tk):
    buttons: list[Button]
    game: Game

    selected: int | None

    OLD_BG: str
    OLD_FG: str

    def __init__(self):
        """Creates the game window"""

        # Set up
        Tk.__init__(self)
        self.title("NumberStack")
        self.resizable(False, False)
        self.option_readfile("dark-mode.txt")

        # Attributes
        self.buttons = []
        self.game = Game(None)
        self.selected = None

        # UI containers
        self.next_frame = LabelFrame(self, text="Next", padx=PADX, pady=PADY, font=SMALL_FONT)
        self.button_grid = LabelFrame(self, text="Grid", padx=PADX, pady=PADY, font=SMALL_FONT)
        self.score_label = Label(self, text="Score: 0", font=SMALL_FONT)
        self.options_box = OptionsBox(self, game=self.game, reload=self.reload)
        
        # Sort out colors
        self.OLD_FG = self.next_frame["fg"]
        self.OLD_BG = self.next_frame["bg"]
        self["bg"] = self.OLD_BG

        # Made so that we can resize buttons via pixels rather than characters
        self.img = PhotoImage(width=1, height=1)

        # Place widgets on screen
        self.button_grid.grid(row=0, column=0, rowspan=5, padx=PADX, pady=PADY, sticky=NSEW)
        self.options_box.grid(row=0, column=1, padx=MENU_PADX, pady=MENU_PADY, sticky=N)
        self.next_frame.grid(row=1, column=1, padx=MENU_PADX, pady=MENU_PADY, sticky=N)
        self.score_label.grid(row=2, column=1, sticky="sew", padx=MENU_PADX, pady=MENU_PADY)
        self.rowconfigure(3, weight=1)

    def reload(self):
        """Reloads the current state"""
        
        self.selected = len(self.game.state.grid) - 1
        self.load_state(self.game.state)

    def load_state(self, state: GameState):
        """Loads a game state"""

        # Get rid of old state
        for button in self.buttons:
            button.destroy()

        if (self.game is not None) and (self.game.state is not None):
            for x in range(self.game.state.width):
                for y in range(self.game.state.height):
                    self.button_grid.rowconfigure(y, weight=0)
                    self.button_grid.columnconfigure(x, weight=0)

        # Internaly load it
        self.game.load_state(state)

        # Create gird buttons
        self.buttons = [
            Button(
                self.button_grid,
                text=str(self.game.state.grid[i]) if self.game.state.grid[i] else " ",
                font=FONT, image=self.img, width=BUTTON_W, height=BUTTON_H, compound="c"
            )
            for i in range(self.game.state.grid_size)
        ]

        # Create next button
        self.buttons.append(
            Button(
                self.next_frame,
                text=str(self.game.state.grid[self.game.state.grid_size]),
                font=FONT, image=self.img, width=BUTTON_W, height=BUTTON_H, compound="c",
                state="disabled",
                disabledforeground=self.OLD_FG
            )
        )

        # Display the next button
        self.buttons[-1].pack()

        # Place and bind the gird buttons
        for x in range(self.game.state.width):
            for y in range(self.game.state.height):
                self.buttons[y * self.game.state.width + x].grid(row=y, column=x, sticky=NSEW, padx=PADX, pady=PADY)
                self.buttons[y * self.game.state.width + x]["command"] = (
                    lambda index=y * self.game.state.width + x: self.combine(index)
                )
                self.buttons[y * self.game.state.width + x].bind(
                    "<ButtonRelease-3>", lambda *event, index=y * self.game.state.width + x: self.select(index)
                )
                self.button_grid.rowconfigure(y, weight=1)
                self.button_grid.columnconfigure(x, weight=1)

        # Select the next button
        self.select(self.game.state.grid_size)

    def update_text(self):
        """Update the text on the buttons aswell as the text color of selected index"""

        # Set buttons back to normal color
        # Set update buttons text
        for i in range(self.game.state.grid_size + 1):
            self.buttons[i].config(
                text=(" " if self.game.state.grid[i] == 0 else str(self.game.state.grid[i])),
                bg=self.OLD_BG,
                fg=self.OLD_FG,
                disabledforeground=self.OLD_FG
            )

        # Set selected text color
        if self.selected is not None:
            self.buttons[self.selected].config(bg=self.OLD_BG, fg=SEL_FG, disabledforeground=SEL_FG)

            # Update other buttons color with the same value as select
            for index in self.game.get_combine_indexes(self.game.state.grid[self.selected]):
                if self.selected != index:
                    self.buttons[index]["bg"] = SAME_BG

        self.score_label["text"] = "Score: " + str(self.game.state.score)

        # Check if the game is over
        if self.game.is_gameover():
            showerror("", "Game Over")

    def select(self, index: int):
        """Selects an index"""
        
        if self.selected is not None and self.selected != self.game.state.grid_size:
            self.buttons[self.selected]["state"] = "normal"

        if self.selected == index:
            self.selected = self.game.state.grid_size
        else:
            self.selected = index
            self.buttons[self.selected]["state"] = "disabled"

        self.update_text()

    def combine(self, index: int):
        """Combines the currently slected index with another"""
        
        if self.selected is not None:
            self.game.combine(self.selected, index)
            self.select(self.game.state.grid_size)

        self.update_text()
