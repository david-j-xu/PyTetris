from enum import Enum
from types import List
import multiprocessing
from pydub import AudioSegment
from pydub.playback import play
import blessed


class TetrominoType(Enum):
    """
    An enum for the types of tetrominos
    """

    """The straight line piece
    """
    I = 1
    """The square piece
    """
    O = 2
    """The T shaped piece
    """
    T = 3
    """The J shaped piece
    """
    J = 3
    """The L shaped piece
    """
    L = 4
    """The S shaped piece
    """
    S = 5
    """The Z shaped piece
    """
    Z = 6


class Tetromino:
    """
    Represents a single tetromino
    """

    def __init__(self, type: TetrominoType) -> None:
        """Creates a tetromino

        Args:
            type (TetrominoType): The type of tetromino
        """
        pass

    def shape() -> List[List[bool]]:
        """Returns how to draw the tetromino, with booleans denoting if it should be drawn

        Returns:
            List[List[bool]]: The shape
        """
        pass

    def rotate_left() -> None:
        """Rotates this tetromino left 90 degrees
        """
        pass

    def rotate_right() -> None:
        """Rotates this tetromino right 90 degrees
        """
        pass

    def __str__(self) -> str:
        """Dunder for to string

        Returns:
            str: the string representation
        """
        pass

    @staticmethod
    def get_shape_of_tetromino(type: TetrominoType) -> List[List[bool]]:
        """Returns the shape of the given type

        Args:
            type (TetrominoType): type of tetromino

        Raises:
            ValueError: On bad input type

        Returns:
            List[List[bool]]: The shape
        """
        match type:
            case TetrominoType.I:
                return [
                    [True, False, False, False],
                    [True, False, False, False],
                    [True, False, False, False],
                    [True, False, False, False],
                ]
            case TetrominoType.O:
                return [
                    [True, True, False],
                    [True, True, False],
                    [False, False, False],
                    [False, False, False],
                ]
            case TetrominoType.T:
                return [
                    [True, True, True],
                    [False, True, False],
                    [False, False, False],
                    [False, False, False],
                ]
            case TetrominoType.J:
                return [
                    [True, False, False],
                    [True, False, False],
                    [True, False, False],
                    [True, False, False],
                ]
            case TetrominoType.L:
                return [
                    [True, False, False],
                    [True, False, False],
                    [True, False, False],
                    [True, False, False],
                ]
            case TetrominoType.S:
                return [
                    [True, False, False],
                    [True, False, False],
                    [True, False, False],
                    [True, False, False],
                ]
            case TetrominoType.Z:
                return [
                    [True, False, False],
                    [True, False, False],
                    [True, False, False],
                    [True, False, False],
                ]
            case _:
                raise ValueError("No type given")


class GameState(Enum):
    """
    An enum for the states the game can be
    """
    TITLE_SCREEN = 1
    GAME_OVER = 2
    PAUSED = 3
    GAME_RUNNING = 4


class Tetris:
    """
    Main class for representing the game of Tetris
    """

    def __init__(self) -> None:
        """Creates a blank game of tetris
        """
        pass

    def generate_piece_bag() -> List[TetrominoType]:
        """Generates the next so many pieces

        Returns:
            List[TetrominoType]: a bag of tetrominos
        """
        pass

    def spawn_piece() -> None:
        """
        Spawns the next piece from the bag
        """
        pass

    def render() -> None:
        """
        Draws the board to the screen
        """
        pass

    def reset() -> None:
        """
        Resets the game
        """
        raise NotImplementedError

    def event_loop() -> None:
        """
        Main game event loop
        """
        raise NotImplementedError
