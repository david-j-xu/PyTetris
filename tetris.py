from enum import Enum
from typing import List
from pydub import AudioSegment
from pydub.playback import play
import blessed
from random import shuffle


class TetrominoType(Enum):
    """
    An enum for the types of tetrominos
    """

    """The straight line piece
    """
    I = "I"
    """The square piece
    """
    O = "O"
    """The T shaped piece
    """
    T = "T"
    """The J shaped piece
    """
    J = "J"
    """The L shaped piece
    """
    L = "L"
    """The S shaped piece
    """
    S = "S"
    """The Z shaped piece
    """
    Z = "Z"
    """None (blank)
    """
    X = "_"

    """Returns the string representation of the enum
    """

    def __str__(self) -> str:
        return self.value


class Tetromino:
    """
    Represents a single tetromino
    """

    def __init__(self, type: TetrominoType) -> None:
        """Creates a tetromino

        Args:
            type (TetrominoType): The type of tetromino
        """
        self.matrix = Tetromino.get_shape_of_tetromino(type)

    def shape(self) -> List[List[TetrominoType]]:
        """Returns how to draw the tetromino, with booleans denoting if it should be drawn

        Returns:
            List[List[TetrominoType]]: The shape
        """
        return self.matrix

    def rotate_left(self) -> None:
        """Rotates this tetromino left 90 degrees
        """
        self.matrix = list(zip(*self.matrix[::]))[::-1]

    def rotate_right(self) -> None:
        """Rotates this tetromino right 90 degrees
        """
        self.matrix = list(zip(*self.matrix[::-1]))

    def __str__(self) -> str:
        """Dunder for to string

        Returns:
            str: the string representation
        """
        string: str = ""
        for row in self.matrix:
            for type in row:
                string += str(type)
            string += "\n"
        return string

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Tetromino):
            return str(self) == str(__value)
        return False

    @staticmethod
    def get_shape_of_tetromino(type: TetrominoType) -> List[List[TetrominoType]]:
        """Returns the shape of the given type

        Args:
            type (TetrominoType): type of tetromino

        Raises:
            ValueError: On bad input type

        Returns:
            List[List[TetrominoType]]: The shape
        """
        t = TetrominoType
        match type:
            case t.I:
                return [
                    [t.X, t.I, t.X, t.X],
                    [t.X, t.I, t.X, t.X],
                    [t.X, t.I, t.X, t.X],
                    [t.X, t.I, t.X, t.X],
                ]
            case t.O:
                return [
                    [t.O, t.O],
                    [t.O, t.O],
                ]
            case t.T:
                return [
                    [t.X, t.T, t.X],
                    [t.T, t.T, t.T],
                    [t.X, t.X, t.X],
                ]
            case t.J:
                return [
                    [t.X, t.J, t.X],
                    [t.X, t.J, t.X],
                    [t.J, t.J, t.X],
                ]
            case t.L:
                return [
                    [t.X, t.L, t.X],
                    [t.X, t.L, t.X],
                    [t.X, t.L, t.L],
                ]
            case t.S:
                return [
                    [t.X, t.S, t.S],
                    [t.S, t.S, t.X],
                    [t.X, t.X, t.X],
                ]
            case t.Z:
                return [
                    [t.Z, t.Z, t.X],
                    [t.X, t.Z, t.Z],
                    [t.X, t.X, t.X],
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
        bag = [Tetromino(type)
               for type in TetrominoType if type != TetrominoType.X]
        shuffle(bag)
        return bag

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
