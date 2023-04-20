from enum import Enum
from typing import List
from pydub import AudioSegment
from pydub.playback import play
from blessed import Terminal
from random import shuffle
import sys
import time


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

    def get_left_boundary(self) -> int:
        """Gets the leftmost column that contains a nonzero value

        Returns:
            int: the leftmost index with something
        """
        for i in range(0, len(self.matrix)):
            column_empty = True
            for j in range(0, len(self.matrix)):
                if self.matrix[j][i] != TetrominoType.X:
                    column_empty = False
            if not column_empty:
                return i

    def get_right_boundary(self) -> int:
        """Gets the rightmost column that contains a nonzero value

        Returns:
            int: the rightmost index with something
        """
        for i in range(len(self.matrix) - 1, -1, -1):
            column_empty = True
            for j in range(0, len(self.matrix)):
                if self.matrix[j][i] != TetrominoType.X:
                    column_empty = False
            if not column_empty:
                return i

    def get_bottom_boundary(self) -> int:
        """Gets the lowest row that contains a nonzero value

        Returns:
            int: the lowest index with something
        """
        for i in range(len(self.matrix) - 1, -1, -1):
            row_empty = True
            for j in range(0, len(self.matrix)):
                if self.matrix[i][j] != TetrominoType.X:
                    row_empty = False
            if not row_empty:
                return i

    def get_size(self) -> int:
        """Returns the size of the block

        Returns:
            int: the side length
        """
        return len(self.matrix)

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

    def __init__(self, term: Terminal) -> None:
        """Creates a blank game of tetris
        """
        self.numRows = 20
        self.numCols = 10
        self.board = [[TetrominoType.X for _ in range(
            self.numCols)] for _ in range(self.numRows)]
        self.term = term
        self.width = None
        self.height = None
        self.calculate_term_dimensions()

        self.curr_block = None
        self.bag = None

    def calculate_term_dimensions(self) -> bool:
        """Recalculates the term dimensions

        Returns:
            bool: True if it's resized from a previous iteration
        """
        if self.term.width != self.width or self.term.height != self.height:
            self.width = self.term.width
            self.height = self.term.height
            self.zero_r = int(.1 * self.height)
            self.block_height = max(1, int(.8 * self.height) // (self.numRows))
            self.block_width = 2 * self.block_height
            self.zero_c = (self.width // 2) - \
                (self.numCols * self.block_width // 2)
            return True
        return False

    def generate_piece_bag(self) -> List[Tetromino]:
        """Generates the next so many pieces

        Returns:
            List[TetrominoType]: a bag of tetrominos
        """
        bag = [Tetromino(type)
               for type in TetrominoType if type != TetrominoType.X]
        shuffle(bag)
        return bag

    def draw_board_border(self) -> None:
        """Draws the border of a board
        """
        # top
        print(self.term.move_xy(self.zero_c - 1, self.zero_r - 1) +
              self.term.on_gray44(
                  "".join([" " for _ in range(self.block_width * self.numCols + 2)])),
              flush=True,
              end="")

        # bottom
        print(self.term.move_xy(self.zero_c - 1, self.zero_r + self.block_height * self.numRows) +
              self.term.on_gray44(
                  "".join([" " for _ in range(self.block_width * self.numCols + 2)])),
              flush=True,
              end="")

        # left
        print("".join(
            [
                self.term.move_xy(
                    self.zero_c - 1, self.zero_r - 1 + i) + self.term.on_gray44(" ")
                for i in range(self.block_height * self.numRows + 2)
            ]
        ), flush=True, end="")

        # right
        print("".join(
            [
                self.term.move_xy(
                    self.zero_c + self.block_width * self.numCols, self.zero_r - 1 + i) + self.term.on_gray44(" ")
                for i in range(self.block_height * self.numRows + 2)
            ]
        ), flush=True, end="")

    def draw_board_coord(self, r: int, c: int, block_type: TetrominoType, ghost: bool = False) -> None:
        """Gets the terminal x, y values of a board coordinate

        Args:
            r (int): the row in board space
            c (int): the column in board space
            block_type (TetrominoType): the type to draw to the screen
            ghost (bool): whether it's a ghost block
        """

        # drawing should be between 10% and 90% height, and then calculate squares from there
        start_r = self.zero_r + r * self.block_height
        end_r = self.zero_r + (r + 1) * self.block_height
        start_c = self.zero_c + c * self.block_width
        end_c = self.zero_c + (c + 1) * self.block_width

        for i in range(start_r, end_r):
            for j in range(start_c, end_c):
                self.draw_space_of_block(block_type, j, i, ghost)

    def draw_curr_block(self) -> None:
        """Draws the moving block (this should be handled separately)
        """
        for i in range(self.curr_block.get_size()):
            for j in range(self.curr_block.get_size()):
                r = self.curr_block_r + i
                c = self.curr_block_c + j
                if r >= 0 and r < self.numRows and c >= 0 and c < self.numCols:
                    if self.curr_block.shape()[i][j] != TetrominoType.X:
                        self.draw_board_coord(
                            r, c, self.curr_block.shape()[i][j])

    def draw_ghost_block(self) -> None:
        """Draws the ghost block (where fast drop would put it)
        """
        for i in range(self.curr_block.get_size()):
            for j in range(self.curr_block.get_size()):
                down_r, down_c = self.find_curr_block_bottom_xy()
                r = down_r + i
                c = down_c + j
                if r >= 0 and r < self.numRows and c >= 0 and c < self.numCols:
                    if self.curr_block.shape()[i][j] != TetrominoType.X:
                        self.draw_board_coord(
                            r, c, self.curr_block.shape()[i][j], True)

    def draw_space_of_block(self, block_type: TetrominoType, x: int, y: int, ghost: bool = False) -> None:
        """Draws one space of the block in terminal space

        Args:
            block_type (TetrominoType): the block type to draw
            x (int): the x value in terminal space
            y (int): the y value in terminal space
            ghost (int): whether it's a ghost
        """
        toDraw = self.term.move_xy(x, y)
        t = TetrominoType
        if not ghost:
            match block_type:
                case t.I:
                    toDraw += self.term.on_cyan(" ")
                case t.O:
                    toDraw += self.term.on_yellow(" ")
                case t.T:
                    toDraw += self.term.on_purple(" ")
                case t.J:
                    toDraw += self.term.on_blue(" ")
                case t.L:
                    toDraw += self.term.on_orange(" ")
                case t.S:
                    toDraw += self.term.on_green4(" ")
                case t.Z:
                    toDraw += self.term.on_red(" ")
                case t.X:
                    toDraw += " "
        else:
            match block_type:
                case t.I | t.O | t.T | t.J | t.L | t.S | t.Z:
                    toDraw += self.term.on_gray89(" ")
                case t.X:
                    toDraw += " "
        print(toDraw, end="", flush=True)

    def render_game(self) -> None:
        """
        Draws the board to the screen
        """
        if self.calculate_term_dimensions():
            # board was resized! clear
            print(self.term.clear, end="", flush=True)

        self.draw_board_border()

        for r, board_row in enumerate(self.board):
            for c, block_type in enumerate(board_row):
                self.draw_board_coord(r, c, block_type)

        self.draw_ghost_block()
        self.draw_curr_block()

        if self.height < self.numRows * 1.20:
            print(self.term.move_xy(self.width // 2 - 15, self.height // 2) +
                  self.term.on_red("Please make your terminal taller!"),
                  end="", flush=True)

    def handle_key(self, key) -> None:
        """Handles a keystroke

        Args:
            key (_type_): the keycode
        """
        term = self.term
        if self.curr_block:
            if key.is_sequence:
                match key.code:
                    case term.KEY_LEFT:
                        self.curr_block_c -= 1
                        if self.curr_block_collides():
                            self.curr_block_c += 1
                        self.maintain_in_boundary()
                    case term.KEY_RIGHT:
                        self.curr_block_c += 1
                        if self.curr_block_collides():
                            self.curr_block_c -= 1
                        self.maintain_in_boundary()
                    case term.KEY_DOWN:
                        self.rotate_curr_left()
                    case term.KEY_UP:
                        self.rotate_curr_right()

            elif key:
                if key.lower() == 'z':
                    self.rotate_curr_left()
                elif key.lower() == 'x':
                    self.rotate_curr_right()
                elif key.lower() == ' ':
                    self.curr_block_r, self.curr_block_c = self.find_curr_block_bottom_xy()

    def maintain_in_boundary(self) -> None:
        """makes sure the current block is in boundary
        """
        if self.curr_block_c > self.numCols - 1 - self.curr_block.get_right_boundary():
            self.curr_block_c = self.numCols - 1 - self.curr_block.get_right_boundary()
        if self.curr_block_c < -self.curr_block.get_left_boundary():
            self.curr_block_c = -self.curr_block.get_left_boundary()

    def rotate_curr_right(self) -> None:
        """Rotates the current block right
        """
        self.curr_block.rotate_right()
        self.maintain_in_boundary()
        if self.curr_block_collides():
            self.curr_block.rotate_left()

    def rotate_curr_left(self) -> None:
        """Rotates the current block left
        """
        self.curr_block.rotate_left()
        self.maintain_in_boundary()
        if self.curr_block_collides():
            self.curr_block.rotate_right()

    def curr_block_collides(self) -> bool:
        """Returns whether the current block collides with some block in the 
        board already

        Returns:
            bool: whether it collides
        """
        return self.block_would_collide(self.curr_block_r, self.curr_block_c)

    def block_would_collide(self, test_r: int, test_c: int) -> bool:
        """Returns whether the current block collides with some block in the 
        board already if it were at test_r, test_c

        Args:
            test_r (int): the test r
            test_c (int): the test c

        Returns:
            bool: whether it collides
        """

        for i in range(self.curr_block.get_size()):
            for j in range(self.curr_block.get_size()):
                r = test_r + i
                c = test_c + j
                # out of bounds
                if self.curr_block.shape()[i][j] != TetrominoType.X and \
                        (r >= self.numRows or c < 0 or c >= self.numCols):
                    return True
                # in bounds
                if (r >= 0 and r < self.numRows and c >= 0 and c < self.numCols) and \
                        self.board[r][c] != TetrominoType.X and \
                        self.curr_block.shape()[i][j] != TetrominoType.X:
                    return True
        return False

    def clear_full_lines(self) -> None:
        """Clears the full lines
        """
        for r in range(self.numRows):
            if all([curr_type != TetrominoType.X for curr_type in self.board[r]]):
                self.board = [[TetrominoType.X for _ in range(
                    self.numCols)]] + self.board[:r] + self.board[r + 1:]

    def find_curr_block_bottom_xy(self) -> tuple([int, int]):
        """Finds the bottommost valid placement. Assumes
        the current placement is valid

        Args:
            self (_type_): self

        Returns:
            tuple([int, int]): (bottomr, bottomc)
        """
        curr_r = self.curr_block_r
        curr_c = self.curr_block_c

        while not self.block_would_collide(curr_r, curr_c):
            curr_r += 1
        # the last one is bad, so backtrack one
        return (curr_r - 1, curr_c)

    def place_curr_block(self) -> None:
        """Places the current block and resets the current block
        """
        for i in range(self.curr_block.get_size()):
            for j in range(self.curr_block.get_size()):
                r = self.curr_block_r + i
                c = self.curr_block_c + j
                if self.curr_block.shape()[i][j] != TetrominoType.X:
                    self.board[r][c] = self.curr_block.shape()[i][j]
        self.curr_block = None

    def event_loop(self) -> None:
        """
        Main game event loop
        """
        LOOP_TIME = .2  # number of seconds for one iteration
        last_time = time.time()
        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor(), self.term.location():
            while True:
                if not self.bag or not len(self.bag):
                    self.bag = self.generate_piece_bag()

                if not self.curr_block:
                    self.curr_block = self.bag.pop()
                    self.curr_block_r = -self.curr_block.get_bottom_boundary() - 2
                    self.curr_block_c = self.numCols // 2
                    if self.block_would_collide(-self.curr_block.get_bottom_boundary(), self.curr_block_c):
                        # collides on spawn? we're dead
                        exit(0)

                if (time.time() > last_time + LOOP_TIME):
                    self.curr_block_r += 1
                    last_time = time.time()

                self.render_game()
                input = self.term.inkey(LOOP_TIME)

                self.handle_key(input)
                if (self.curr_block_r, self.curr_block_c) == self.find_curr_block_bottom_xy():
                    self.place_curr_block()
                    self.clear_full_lines()
