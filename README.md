# PyTetris

## Project Description
This is an implementation of the game Tetris that is completely contained within the terminal. The idea was just to make something that you can play while you're in your terminal, where you don't need to have too many extra things to install and which doesn't open any additional windows. I chose to implement this since Tetris is, from the outside, a really simple game -- you just stack blocks on top of each other, and I thought that the simplicity really fit with the "play everything in your terminal" vibe. However, the actual mechanics can be a bit more complex, and I thought it'd be fun to write.

To implement the game, I used the `blessed` third-party module, which allows me to write to the terminal screen. I wrote my own renderers/drivers for this in order to render the blocks and the screen for tetris. In my development, I found it useful to use the native libraries for `typing` and `enum` in order to add a bit of type checking as well as support for enumerated types. I also developed a few unit tests using the `unittest` module to test my tetromino implementation. In addition to the core gameplay, which ends whenever you stack above the end of the screen, I've added a few additional features in order to satisfy the implementation requirements. I've added dunder methods in all my classes, with each of them having an `__init__`, as well as some `__eq__` and `__str__` classes for debugging. I also added music, which I wrote and recorded by hand using samples from people I know. This is played using my second third party module, `playsound`, which does a blocking play in a secondary thread, which I create and manage using the `threading` native module. I've also added `argparse` with a `-m`/`--music` flag to turn on music (since while it adds to the ambience, I'm not sure I want it all the time!).

## Installation Instructions
The only dependencies you need are `blessed` and `playsound`, which can be acquired through `pip` normally (`pip install blessed playsound`). You will also need a terminal that can support a decent amount of colors (I'm using iTerm for this, but basically every terminal should work, though I can't really try it). I am running on python 3.10, which I think might be necessary (as the code relies on pattern matching).

In order to run the application, navigate such that your `pwd` is this directory. Then, run `python3 main.py` with or without the optional `-m` argument (if you want to hear the music).

## Code Structure
I have three main files:
- `main.py`: This is the main entry point of my program. It handles the argument parsing as well as the thread management for playing music. It also initializes the game.
- `tetris.py`: This is the meat of the program. It contains the `TetrominoType` enum, which has the types for the tetrominos. It also has a class for `Tetromino`, which contains the rotation logic and all the other logic for keeping track of tetromino shapes. Lastly it has the `Tetris` class, which handles the game logic, including handling the board and rendering it to the terminal.
- `test.py`: these are just a few unit tests to validate some tetromino logic