from Juego import Game
from lectura_mapa import read_map_from_file
import sys

def backtracking_algorithm(game: Game):
    """
    Solves the Bridges game using backtracking.
    Modifies the game object in place.
    Returns True if a solution is found, False otherwise.
    """
    
    # 1. Identify all islands
    rows = game.rows
    cols = game.cols
    islands = []
    for r in range(rows):
        for c in range(cols):
            if game.matrix[r][c] > 0:
                islands.append((r, c))

    if not islands:
        return False
    
    # 2. Generate all potential bridges (edges) between islands
    # We only need to look for neighbors to the right and below to avoid duplicates
    potential_bridges = []
    
    for i, (r1, c1) in enumerate(islands):
        for j in range(i + 1, len(islands)):
            r2, c2 = islands[j]
            
            # Check if they are aligned
            if r1 == r2: # Horizontal
                # Check if path is clear (no islands in between)
                # The is_valid_bridge check in Game class handles crossing other bridges and islands
                # But we can do a quick check here to filter obvious candidates
                if game.is_valid_bridge((r1, c1), (r2, c2)):
                     potential_bridges.append(((r1, c1), (r2, c2)))
            elif c1 == c2: # Vertical
                if game.is_valid_bridge((r1, c1), (r2, c2)):
                    potential_bridges.append(((r1, c1), (r2, c2)))

    # 3. Recursive backtracking function
    def solve(index):
        # Base case: Check if the game is solved
        if game.is_solved():
            return True
        
        # If we ran out of potential bridges to consider, and not solved, then fail
        if index >= len(potential_bridges):
            return False
            
        u, v = potential_bridges[index]
        
        # Try adding 0, 1, or 2 bridges
        # We try 2 first, then 1, then 0 (greedy approach might be faster, or not)
        # Actually, let's try 0, 1, 2. Or maybe 2, 1, 0.
        # Let's try to satisfy constraints.
        
        # Option 1: Add 2 bridges
        if game.is_valid_bridge(u, v):
            game.add_bridge(u, v)
            # Try adding a second one
            if game.is_valid_bridge(u, v):
                game.add_bridge(u, v)
                if solve(index + 1):
                    return True
                game.delete_bridge(u, v) # Backtrack 2nd
            
            # If 2 didn't work (or couldn't place 2nd), we are here with 1 bridge placed.
            # Check if 1 bridge leads to solution
            if solve(index + 1):
                return True
            
            game.delete_bridge(u, v) # Backtrack 1st
            
        # Option 2: Add 0 bridges (skip this connection)
        if solve(index + 1):
            return True
            
        return False

    # Start recursion
    if solve(0):
        print("Solution found!")
        game.print_game_state()
        return True
    else:
        print("No solution found for this map.")
        game.print_game_state()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python algoritmo.py <mapa.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    matrix = read_map_from_file(filename)
    game = Game(matrix)
    backtracking_algorithm(game)