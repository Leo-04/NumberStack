from random import randint as rand
from tkinter import *
from game import Game
from tkinter.filedialog import *
from new_game_win import NewGameWin


class OptionsBox(Frame):
    game: Game | None
    new_game_win: NewGameWin

    def __init__(self, *args, game=None, reload=lambda: None, **kwargs):
        """Creates a box with soem buttons"""
        
        Frame.__init__(self, *args, **kwargs)

        self.game = game

        # Create buttons
        self.new_button = Button(self, text="New", command=self.new)
        self.load_button = Button(self, text="Load", command=self.load)
        self.save_button = Button(self, text="Save", command=self.save)

        # Create an instance of the new game window popup
        self.new_win = NewGameWin(self.winfo_toplevel())
        self.new_win.overrideredirect(True)
        self.new_win.config(bd=3, relief="raised")
        self.new_win.bind("<FocusOut>", lambda e: self.new_win.cancel())

        # Show buttons on screen
        self.new_button.pack(fill=BOTH, expand=1, pady=(20, 0))
        self.load_button.pack(fill=BOTH, expand=1, pady=(20, 0))
        self.save_button.pack(fill=BOTH, expand=1, pady=(20, 0))

        # Bind hotkeys
        self.bind_all("<Control-s>", lambda e: self.save())
        self.bind_all("<Control-n>", lambda e: self.new())
        self.bind_all("<Control-o>", lambda e: self.load())

        self.reload = reload

    def new(self):
        """Callback for new game button"""
        
        self.new_win.geometry("+%s+%s" % (
            self.winfo_toplevel().winfo_x() + self.winfo_toplevel().winfo_width() // 2 - self.new_win.winfo_width() // 2,
            self.winfo_toplevel().winfo_y() + self.winfo_toplevel().winfo_height() // 2 - self.new_win.winfo_height() // 2
        ))
        w, h = self.new_win.ask_options()

        if w is not None:
            # load new game
            self.game.state.grid = [0 for i in range(w*h)]
            self.game.state.grid.append(rand(1, 2))
            self.game.state.width = w
            self.game.state.height = h
            self.game.state.score = 0
            self.reload()

    def load(self):
        """Callback for load game button"""
        
        filename = askopenfilename(defaultextension=".json", filetypes=(("Json", "*.json"), ("Any", "*.*")))

        if filename:
            # open game
            with open(filename, "r") as fp:
                json_str = fp.read()

            # load game
            self.game.state.from_json(json_str)
            self.reload()

    def save(self):
        """Callback for save game button"""
        
        filename = asksaveasfilename(defaultextension=".json", filetypes=(("Json", "*.json"), ("Any", "*.*")))

        if filename:
            # get json
            json_str = self.game.state.to_json()

            # save json
            with open(filename, "w") as fp:
                fp.write(json_str)

            self.reload()
