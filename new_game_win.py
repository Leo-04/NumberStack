import tkinter.ttk
from tkinter import *


class NewGameWin(Toplevel):
    def __init__(self, root=None):
        # Setup window
        Toplevel.__init__(self, root)
        self.title("New Game")
        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.resizable(False, False)
        self.geometry("200x210")

        # Create sliders
        self.width = Scale(self, from_=1, to=10, showvalue=True, tickinterval=1, label="Width", orient=HORIZONTAL)
        self.width.set(4)
        self.width.pack(fill=BOTH, expand=1)
        self.height = Scale(self, from_=1, to=10, showvalue=True, tickinterval=1, label="Height", orient=HORIZONTAL)
        self.height.set(4)
        self.height.pack(fill=BOTH, expand=1)

        # Create buttons
        self.ok_button = Button(self, text="Ok", command=self.ok, padx=10, pady=10)
        self.cancel_button = Button(self, text="Cancel", command=self.cancel, padx=10, pady=10)
        self.ok_button.pack(side=LEFT, anchor=W, padx=10, pady=10)
        self.cancel_button.pack(side=RIGHT, anchor=E, padx=10, pady=10)

        # Bind macros
        self.bind_all("<Return>", lambda e: self.ok())
        self.bind_all("<Escape>", lambda e: self.cancel())

        self.flag = None

    def ok(self):
        self.withdraw()
        if self.flag is None:
            self.flag = True

    def cancel(self):
        self.withdraw()
        if self.flag is None:
            self.flag = False

    def ask_options(self):
        """Shows popup and waits for user to select options"""

        # Show window
        self.deiconify()
        self.update()
        self.focus()

        # Wait for responce
        self.flag = None
        while self.flag is None:
            self.update()

        # Return responce
        if self.flag:
            return self.width.get(), self.height.get()
        else:
            return None, None
