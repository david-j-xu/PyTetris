from tetris import Tetris
import threading
import playsound
import argparse
from blessed import Terminal


def start_music():
    def play_music_on_loop():
        while True:
            # should block the background thread
            playsound.playsound('tetris.mp3', True)
    sound_thread = threading.Thread(target=play_music_on_loop)
    sound_thread.daemon = True
    sound_thread.start()


def main(play_music: bool):
    """
    The main runner of the game
    """

    term = Terminal()
    tetris = Tetris(term)
    if play_music:
        start_music()
    tetris.event_loop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="play tetris in the terminal!")
    parser.add_argument(
        '-m', '--music', action='store_true', help="Play music!")
    args = parser.parse_args()
    main(args.music)
