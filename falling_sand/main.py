import pygame
import random


def drop_sand(row, col) -> None:
    for i in range(-DROP_RADIUS + 1, DROP_RADIUS):
        for j in range(-DROP_RADIUS + 1, DROP_RADIUS):
            shifted_row, shifted_col = row + i, col + j
            if shifted_row < 0 or shifted_row >= ROWS or \
               shifted_col < 0 or shifted_col >= COLS or \
               ((shifted_row - row)**2 + (shifted_col - col)**2)**0.5 >= DROP_RADIUS:
                continue
            grid[shifted_row][shifted_col] = int(hue)


def update_grid() -> None:
    global grid
    new_grid = [[0] * COLS for _ in range(ROWS)]
    for row in range(0, ROWS):
        for col in range(0, COLS):
            # No sand to move
            if not grid[row][col]: continue

            # Sand grain can keep falling down
            if row < ROWS - 1 and grid[row+1][col] == 0:
                new_grid[row+1][col] = grid[row][col]

            else:
                side_options = []
                # Sand grain can fall to the bottom-right side
                if row < ROWS - 1 and col < COLS - 1 and grid[row+1][col+1] == 0:
                    side_options.append((row+1, col+1))

                # Sand grain can fall to the bottom-left side
                if row < ROWS - 1 and col > 0 and grid[row+1][col-1] == 0:
                    side_options.append((row+1, col-1))

                if not side_options: 
                    new_grid[row][col] = grid[row][col]
                else:
                    side_cell = random.choice(side_options)
                    new_grid[side_cell[0]][side_cell[1]] = grid[row][col]
    grid = new_grid



def draw_grid() -> None:
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] != 0: 
                draw_cell(row, col)

    
def draw_cell(row: int, col: int) -> None:
    rect = pygame.Rect(col * COL_SIZE, row * ROW_SIZE, COL_SIZE, ROW_SIZE)
    sand_color.hsva = (grid[row][col], 100, 100, 100)
    pygame.draw.rect(screen, sand_color, rect)


WIDTH = 500
HEIGHT = 500
ROWS = 250
COLS = 250
DROP_RADIUS = 5
ROW_SIZE = HEIGHT // ROWS
COL_SIZE = WIDTH // COLS

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

grid = [[0] * COLS for _ in range(ROWS)]
sand_color = pygame.Color(0)
hue = 1

running = True
pressed = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    screen.fill('black')

    # for i in range(ROWS):
    #     pygame.draw.line(screen, 'white', (0, i * ROW_SIZE),(WIDTH, i * ROW_SIZE))

    # for i in range(COLS):
    #     pygame.draw.line(screen, 'white', (i * COL_SIZE, 0),(i * COL_SIZE, HEIGHT))

    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        event_row = y // ROW_SIZE
        event_col = x // COL_SIZE
        drop_sand(event_row, event_col)

        hue += 0.2
        if hue > 360: hue = 1

    update_grid()
    draw_grid()

    pygame.display.update()
    clock.tick(90)

pygame.quit()