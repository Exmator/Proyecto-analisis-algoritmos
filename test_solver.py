import unittest
from Juego import Game
from algoritmo import backtracking_algorithm
from lectura_mapa import read_map_from_file


class TestBacktracking(unittest.TestCase):
    def test_simple_solvable(self):
        print("\n--- Test Simple Solvable ---")
        # 2 islands needing 2 connections each, horizontal
        matrix = [
            [2, 0, 2],
            [0, 0, 0],
            [0, 0, 0]
        ]
        game = Game(matrix)
        result = backtracking_algorithm(game)
        self.assertTrue(result)
        print("Bridges:", game.bridges)
        self.assertTrue(game.is_solved())

    def test_vertical_solvable(self):
        print("\n--- Test Vertical Solvable ---")
        # 2 islands needing 1 connection each, vertical
        matrix = [
            [1, 0, 0],
            [0, 0, 0],
            [1, 0, 0]
        ]
        game = Game(matrix)
        result = backtracking_algorithm(game)
        self.assertTrue(result)
        print("Bridges:", game.bridges)
        self.assertTrue(game.is_solved())

    def test_l_map(self):
        print("\n--- Test L Map ---")
        # L shape map
        matrix = [
            [1, 0, 0],
            [0, 0, 0],
            [3, 0, 2]
        ]
        game = Game(matrix)
        result = backtracking_algorithm(game)
        self.assertTrue(result)
        print("Bridges:", game.bridges)
        self.assertTrue(game.is_solved())

    def test_5_islands(self):
        print("\n--- Test 5 Islands ---")
        # 5 islands needing 1 connection each
        matrix = [
            [0, 1, 0],
            [1, 4, 1],
            [0, 1, 0]
        ]
        game = Game(matrix)
        result = backtracking_algorithm(game)
        self.assertTrue(result)
        print("Bridges:", game.bridges)
        self.assertTrue(game.is_solved())
    
    def test_imposible_all_islands(self):
        print("\n--- Test Impossible All Islands ---")
        # All islands needing 1 connection each, but no neighbors
        matrix = [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ]
        game = Game(matrix)
        result = backtracking_algorithm(game)
        self.assertFalse(result)

    def test_impossible_isolated_islands(self):
        print("\n--- Test Impossible Isolated Islands ---")
        # 2 islands needing 1 connection each, but no neighbors
        matrix = [
            [1, 1, 0],
            [0, 0, 2],
            [0, 0, 2]
        ]
        game = Game(matrix)
        result = backtracking_algorithm(game)
        self.assertFalse(result)

    def test_impossible_isolated(self):
        print("\n--- Test Impossible Isolated ---")
        # 1 island needing 1 connection, but no neighbors
        matrix = [
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        game = Game(matrix)
        result = backtracking_algorithm(game)
        self.assertFalse(result)
        
    def test_impossible_parity(self):
        print("\n--- Test Impossible Parity ---")
        # 2 islands, one needs 1, other needs 2. Impossible to satisfy both fully if they only connect to each other.
        matrix = [
            [1, 0, 2],
            [0, 0, 0],
            [0, 0, 0]
        ]
        game = Game(matrix)
        result = backtracking_algorithm(game)
        self.assertFalse(result)

    def test_impossible_diagonal(self):
        print("\n--- Test Impossible Diagonal ---")
        # 2 islands needing 1 connection each, diagonal
        matrix = [
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 2]
        ]
        game = Game(matrix)
        result = backtracking_algorithm(game)
        self.assertFalse(result)

    def test_easy_file(self):
        print("\n--- Test Easy File ---")
        matrix = read_map_from_file("easy.txt")
        game = Game(matrix)
        result = backtracking_algorithm(game)
        self.assertTrue(result)
        self.assertTrue(game.is_solved())

    def test_medium_file(self):
        print("\n--- Test Medium File ---")
        matrix = read_map_from_file("medium.txt")
        game = Game(matrix)
        result = backtracking_algorithm(game)
        self.assertTrue(result)
        self.assertTrue(game.is_solved())
    
    def test_empty_file(self):
        print("\n--- Test Empty File ---")
        matrix = read_map_from_file("empty.txt")
        game = Game(matrix)
        result = backtracking_algorithm(game)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()

