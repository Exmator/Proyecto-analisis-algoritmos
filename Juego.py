class Game:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.bridges = []  # List of tuples: ((x1, y1), (x2, y2), count)

    # Helper to check if a bridge crosses another bridge
    def _crosses_bridge(self, point, bridge):
        (x1, y1), (x2, y2), _ = bridge
        if x1 == x2 == point[0]:
            return min(y1, y2) < point[1] < max(y1, y2)
        if y1 == y2 == point[1]:
            return min(x1, x2) < point[0] < max(x1, x2)
        return False

    # Check if two coordinates are connected by the same bridge
    def _same_edge(self, coord1, coord2, bridge):
        """Return True if bridge connects the same two coordinates (order insensitive)."""
        a, b, _ = bridge
        return {a, b} == {coord1, coord2}

    # Check if a bridge can be placed between two coordinates
    def is_valid_bridge(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2

        # Must be aligned horizontally or vertically
        if x1 != x2 and y1 != y2:
            print("Bridges must be horizontal or vertical.")
            return False

        # Must be different coordinates
        if (x1, y1) == (x2, y2):
            print("Cannot place a bridge on the same island.")
            return False

        # Must both be islands (nonzero)
        if self.matrix[x1][y1] == 0 or self.matrix[x2][y2] == 0:
            print("Both endpoints must be islands.")
            return False

        # Walk the cells between the islands (exclusive of endpoints)
        if x1 == x2:
            # horizontal (same row, varying column)
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                # Can't pass through other islands
                if self.matrix[x1][y] != 0:
                    print("Bridges cannot pass through islands.")
                    return False
                # Can't cross an existing bridge — but ignore the bridge that connects these two islands
                for b in self.bridges:
                    if self._same_edge(coord1, coord2, b):
                        continue
                    if self._crosses_bridge((x1, y), b):
                        print("Bridge crossing detected with:", b)
                        return False
        else:
            # vertical (same column, varying row)
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if self.matrix[x][y1] != 0:
                    print("Bridges cannot pass through islands.")
                    return False
                for b in self.bridges:
                    if self._same_edge(coord1, coord2, b):
                        continue
                    if self._crosses_bridge((x, y1), b):
                        print("Bridge crossing detected with:", b)
                        return False

        # Also ensure that adding this bridge would not exceed either island's required degree.
        # Count existing connections for each endpoint:
        a_conn = sum(count for (a, b, count) in self.bridges if a == (x1, y1) or b == (x1, y1))
        b_conn = sum(count for (a, b, count) in self.bridges if a == (x2, y2) or b == (x2, y2))

        # If there's already 2 bridges between these two islands, is_valid_bridge should be False.
        for (a, b, count) in self.bridges:
            if {a, b} == {coord1, coord2} and count >= 2:
                return False

        # Check target island capacities (can't exceed the number on the island)
        if a_conn + 1 > self.matrix[x1][y1] or b_conn + 1 > self.matrix[x2][y2]:
            return False

        return True
    # Add a bridge between two coordinates
    def add_bridge(self, coord1, coord2):
        if not self.is_valid_bridge(coord1, coord2):
            return False

        # Check if a bridge already exists (double bridge case)
        for i, (a, b, count) in enumerate(self.bridges):
            if {a, b} == {coord1, coord2}:
                if count < 2:
                    self.bridges[i] = (a, b, count + 1)
                    return True
                else:
                    print("Maximum of 2 bridges already placed.")
                    return False
        # Add new bridge
        self.bridges.append((coord1, coord2, 1))
        return True
    
    # Remove a bridge between two coordinates
    def delete_bridge(self, coord1, coord2):
        for i, (a, b, count) in enumerate(self.bridges):
            if {a, b} == {coord1, coord2}:
                if count > 1:
                    self.bridges[i] = (a, b, count - 1)
                else:
                    self.bridges.pop(i)
                return True
        print("No bridge exists between", coord1, "and", coord2)
        return False

    # Check if the current game state is solved
    def is_solved(self):
        # Count bridges connected to each island
        connection_count = [[0] * self.cols for _ in range(self.rows)]

        for (a, b, count) in self.bridges:
            x1, y1 = a
            x2, y2 = b
            connection_count[x1][y1] += count
            connection_count[x2][y2] += count

        # Verify each island
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j] > 0:
                    if connection_count[i][j] != self.matrix[i][j]:
                        return False
        return True
    
    # Getters
    def get_map(self):
        return self.matrix
    def get_bridges(self):
        return self.bridges
