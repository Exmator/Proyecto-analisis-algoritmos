import pygame
import sys
from math import sqrt
from Juego import Game
from lectura_mapa import read_map_from_file

pygame.init()
FONT = pygame.font.SysFont("arial", 28)
WIDTH, HEIGHT = 700, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hashiwokakero (Bridges Game)")

# Colors
WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (80, 80, 255)

# ====== Helper Functions ======
def draw_game(game, selected=None):
    SCREEN.fill(WHITE)
    spacing = WIDTH // (game.cols + 2)
    coords = {}

    # Draw bridges
    for (a, b, count) in game.bridges:
        (x1, y1), (x2, y2) = a, b
        p1 = (y1 * spacing + spacing, x1 * spacing + spacing)
        p2 = (y2 * spacing + spacing, x2 * spacing + spacing)
        if count == 1:
            pygame.draw.line(SCREEN, GRAY, p1, p2, 6)
        else:
            # Two parallel lines (offset by 5 px)
            if x1 == x2:  # horizontal
                pygame.draw.line(SCREEN, GRAY, (p1[0], p1[1] - 5), (p2[0], p2[1] - 5), 5)
                pygame.draw.line(SCREEN, GRAY, (p1[0], p1[1] + 5), (p2[0], p2[1] + 5), 5)
            else:  # vertical
                pygame.draw.line(SCREEN, GRAY, (p1[0] - 5, p1[1]), (p2[0] - 5, p2[1]), 5)
                pygame.draw.line(SCREEN, GRAY, (p1[0] + 5, p1[1]), (p2[0] + 5, p2[1]), 5)

    # Draw islands
    for i in range(game.rows):
        for j in range(game.cols):
            val = game.matrix[i][j]
            if val > 0:
                x = j * spacing + spacing
                y = i * spacing + spacing
                color = BLUE if selected == (i, j) else BLACK
                pygame.draw.circle(SCREEN, color, (x, y), 25)
                text = FONT.render(str(val), True, WHITE)
                SCREEN.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
                coords[(i, j)] = (x, y)

    return coords


def find_clicked_island(mouse_pos, coords):
    for (i, j), (x, y) in coords.items():
        if sqrt((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2) <= 25:
            return (i, j)
    return None


def find_clicked_bridge(mouse_pos, game, coords):
    mx, my = mouse_pos
    for (a, b, _) in game.bridges:
        (x1, y1) = coords[a]
        (x2, y2) = coords[b]

        # Check bounding box first (quick reject)
        if not (min(x1, x2) - 10 <= mx <= max(x1, x2) + 10 and
                min(y1, y2) - 10 <= my <= max(y1, y2) + 10):
            continue

        # Compute perpendicular distance from point to line segment
        dx, dy = x2 - x1, y2 - y1
        if dx == dy == 0:
            continue  # same point — shouldn't happen

        # Project mouse onto segment parameter t in [0,1]
        t = ((mx - x1) * dx + (my - y1) * dy) / float(dx * dx + dy * dy)
        if 0 <= t <= 1:
            # Closest point on segment
            px, py = x1 + t * dx, y1 + t * dy
            dist = sqrt((mx - px) ** 2 + (my - py) ** 2)
            if dist < 10:  # click within 10 pixels of segment
                return (a, b)
    return None


# ====== Main Game Loop ======
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python usuario.py <mapa.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    matrix = read_map_from_file(filename)
    game = Game(matrix)

    running = True
    selected = None

    while running:
        coords = draw_game(game, selected)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Try to detect clicked island
                clicked = find_clicked_island(mouse_pos, coords)
                if clicked:
                    if not selected:
                        selected = clicked
                    else:
                        if clicked == selected:
                            selected = None
                        else:
                            game.add_bridge(selected, clicked)
                            selected = None
                else:
                    # Try to detect bridge click (for deletion)
                    b = find_clicked_bridge(mouse_pos, game, coords)
                    if b:
                        game.delete_bridge(*b)
            if game.is_solved():
                print("¡Felicidades! Has resuelto el juego.")
                running = False

    pygame.quit()