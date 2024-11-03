import sys
import os
import unittest
from colorama import Fore, Style
import numpy as np

# Add the directory above to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the Connect4Board class
from game import Connect4Board  # Adjust based on your actual class name


class CustomTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        # Extract the simple test method name
        test_name = test.id().split('.')[-1]
        self.stream.write(Fore.GREEN + f"{test_name} : PASSED\n" + Style.RESET_ALL)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        # Extract the simple test method name
        test_name = test.id().split('.')[-1]
        self.stream.write(Fore.RED + f"{test_name} : FAILED\n" + Style.RESET_ALL)

    def addError(self, test, err):
        super().addError(test, err)
        # Extract the simple test method name
        test_name = test.id().split('.')[-1]
        self.stream.write(Fore.RED + f"{test_name} : ERROR\n" + Style.RESET_ALL)

class CustomTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTestResult(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        # Suppress the default output
        result = self._makeResult()
        test(result)
        return result

class TestConnect4Board(unittest.TestCase):

    # Initialization Tests
    def test_initial_board(self):
        b = Connect4Board()
        expected_board = np.zeros((6, 7), dtype=int)
        np.testing.assert_array_equal(b.board, expected_board)
    
    def test_initial_player(self):
        b = Connect4Board()
        np.testing.assert_equal(b.current_player, 1)
    
    # Drop pieces Tests
    def test_drop_piece1(self):
        b = Connect4Board()
        b.drop_piece(0)
        np.testing.assert_equal(b.board[0,0], 1)
    
    def test_drop_piece2(self):
        b = Connect4Board()
        b.drop_piece(6)
        np.testing.assert_equal(b.board[0,6], 1)
            
    def test_drop_piece3(self):
        b = Connect4Board()
        b.drop_piece(0)
        b.drop_piece(3)
        b.drop_piece(3)
        b.drop_piece(3)
        b.drop_piece(2)
        expected = np.array([[1,0,1,1,0,0,0],
                             [0,0,0,1,0,0,0],
                             [0,0,0,1,0,0,0],
                             [0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0]])
        np.testing.assert_array_equal(b.board, expected)
    
    def test_drop_piece4(self):
        b = Connect4Board()
        for _ in range(6):
            for j in range(7):
                b.drop_piece(j)
        expected = np.ones((6,7), dtype=int)
        np.testing.assert_array_equal(b.board, expected)

    # Error checking
    def test_invalid_drop_piece_invalid_column(self):
        b = Connect4Board()
        with self.assertRaises(ValueError) as context:
            b.drop_piece(7)  # Attempt to drop a piece in an invalid column
        self.assertEqual(str(context.exception), "Invalid Column")

    def test_invalid_drop_piece_full_column(self):
        b = Connect4Board()
        
        # Fill the column
        for _ in range(6):
            b.drop_piece(0)  # Fill the first column

        with self.assertRaises(ValueError) as context:
            b.drop_piece(0)  # Attempt to drop a piece in a full column
        self.assertEqual(str(context.exception), "Column is full")

    # Switch Player
    def test_switch_player1(self):
        b = Connect4Board()
        b.switch_player()
        self.assertEqual(b.current_player, 2)

    def test_switch_player2(self):
        b = Connect4Board()
        b.switch_player()
        b.switch_player()
        self.assertEqual(b.current_player, 1)

    # Check for win
    def test_check_win1(self):
        b = Connect4Board()
        b.board = np.array([[1,0,1,1,0,0,0],
                            [0,0,0,1,0,0,0],
                            [0,0,0,1,0,0,0],
                            [0,0,0,1,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0]])
        win = b.check_for_win(player=1)
        expected = (True, [(0,3), (1,3), (2,3), (3,3)])
        self.assertEqual(win, expected)

    def test_check_win2(self):
        b = Connect4Board()
        b.board = np.array([[1,0,1,1,0,0,0],
                            [0,1,0,0,0,0,0],
                            [0,0,1,1,0,0,0],
                            [0,0,0,1,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0]])
        win = b.check_for_win(player=1)
        expected = (True, [(0,0), (1,1), (2,2), (3,3)])
        self.assertEqual(win, expected)
    
    def test_check_win3(self):
        b = Connect4Board()
        b.board = np.array([[1,1,1,1,0,0,0],
                            [0,1,0,0,0,0,0],
                            [0,0,0,1,0,0,0],
                            [0,0,0,1,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0]])
        win = b.check_for_win(player=1)
        expected = (True, [(0,0), (0,1), (0,2), (0,3)])
        self.assertEqual(win, expected)

    def test_check_win4(self):
        b = Connect4Board()
        b.board = np.array([[1,0,1,1,0,0,1],
                            [0,1,0,0,0,1,0],
                            [0,0,0,1,1,0,0],
                            [0,0,0,1,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0]])
        win = b.check_for_win(player=1)
        expected = (True, [(3,3), (2,4), (1,5), (0,6)])
        self.assertEqual(win, expected)

    def test_check_win5(self):
        b = Connect4Board()
        b.board = np.array([[1,0,1,1,0,0,1],
                            [0,1,0,0,0,1,0],
                            [0,0,0,1,1,0,0],
                            [0,0,0,1,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0]])
        win = b.check_for_win(player=2)
        expected = (False, None)
        self.assertEqual(win, expected)



if __name__ == '__main__':
    # Initialize colorama
    from colorama import init
    init(autoreset=True)

    # Run the tests with the custom test runner
    runner = CustomTestRunner(verbosity=0)  # Set verbosity to 0 to suppress default output
    result = runner.run(unittest.TestLoader().loadTestsFromTestCase(TestConnect4Board))

    # Final output summary
    print(f"\nTotal tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
