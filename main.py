from tetris import Tetris
from blessed import Terminal


def main():
    """
    The main runner of the game
    """
    term = Terminal()
    tetris = Tetris(term)
    tetris.event_loop()


if __name__ == "__main__":
    main()
