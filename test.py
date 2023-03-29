import unittest
from tetris import TetrominoType, Tetromino


class TestTetromino(unittest.TestCase):
    def test_rotate_left_identity(self):
        for type in TetrominoType:
            if type == TetrominoType.X:
                continue
            rotate = Tetromino(type)
            rotate.rotate_left()
            rotate.rotate_left()
            rotate.rotate_left()
            rotate.rotate_left()
            self.assertEqual(rotate, Tetromino(type))

    def test_rotate_right_identity(self):
        for type in TetrominoType:
            if type == TetrominoType.X:
                continue
            rotate = Tetromino(type)
            rotate.rotate_right()
            rotate.rotate_right()
            rotate.rotate_right()
            rotate.rotate_right()
            self.assertEqual(rotate, Tetromino(type))

    def test_rotate_inverse(self):
        for type in TetrominoType:
            if type == TetrominoType.X:
                continue
            rotate = Tetromino(type)
            rotate.rotate_left()
            rotate.rotate_right()
            rotate.rotate_right()
            rotate.rotate_left()
            self.assertEqual(rotate, Tetromino(type))


if __name__ == '__main__':
    unittest.main()
