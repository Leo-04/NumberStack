from game_window import GameWindow, GameState, Tk


def main():
    win = GameWindow()
    win.load_state(GameState(4, 4, 0, [
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        1
    ]))

    win.mainloop()


if __name__ == "__main__":
    main()
