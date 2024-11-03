import unittest
from colorama import Fore, Style
import numpy as np
from game import Connect4Board  # Make sure to adjust this import based on your project structure

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

    def setUp(self):
        self.board = Connect4Board()

    def test_initial_board(self):
        expected_board = np.zeros((6, 7), dtype=int)
        np.testing.assert_array_equal(self.board.board, expected_board)

    def test_drop_piece(self):
        self.board.board[5, 3] = 1  # Simulate dropping a piece
        self.assertEqual(self.board.board[5, 3], 1)

    def test_check_for_win_horizontal(self):
        self.board.board[5] = [1, 1, 1, 1, 0, 0, 0]  # Horizontal win
        self.assertEqual(self.board.check_for_win(1), (True, [(5, 0), (5, 1), (5, 2), (5, 3)]))

    def test_check_for_win_vertical(self):
        self.board.board[2:6, 3] = 1  # Vertical win
        self.assertEqual(self.board.check_for_win(1), (True, [(2, 3), (3, 3), (4, 3), (5, 3)]))

    def test_check_for_win_diagonal(self):
        self.board.board[2, 2] = 1
        self.board.board[3, 3] = 1
        self.board.board[4, 4] = 1
        self.board.board[5, 5] = 1  # Positive diagonal win
        self.assertEqual(self.board.check_for_win(1), (True, [(2, 2), (3, 3), (4, 4), (5, 5)]))

    def test_no_win(self):
        self.assertEqual(self.board.check_for_win(1), (False, None))

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
