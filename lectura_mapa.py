def read_map_from_file(filename):
    with open(filename, 'r') as file:
        # Read map dimensions
        first_line = file.readline().strip()
        rows, cols = map(int, first_line.split(','))

        # Read map
        game_map = []
        for _ in range(rows):
            line = file.readline().strip()
            # Convert each character to an integer
            row = [int(ch) for ch in line]
            game_map.append(row)
    return game_map

if __name__ == "__main__":
    filename = "map.txt"  # File containing the map data
    game_map = read_map_from_file(filename)

    print("Map:")
    for row in game_map:
        print(row)
