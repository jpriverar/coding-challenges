import pygame


def update_grid() -> None:
    for row in range(ROWS-1, -1, -1):
        for col in range(COLS-1, -1, -1):
            # No sand to move
            if not grid[row][col]: continue

            # Sand grain can keep falling down
            if row < ROWS - 1 and grid[row+1][col] == 0:
                grid[row][col], grid[row+1][col] = grid[row+1][col], grid[row][col]

            # Sand grain can fall to the bottom-right side
            elif row < ROWS - 1 and col < COLS - 1 and grid[row+1][col+1] == 0:
                grid[row][col], grid[row+1][col+1] = grid[row+1][col+1], grid[row][col]

            # Sand grain can fall to the bottom-left side
            elif row < ROWS - 1 and col > 0 and grid[row+1][col-1] == 0:
                grid[row][col], grid[row+1][col-1] = grid[row+1][col-1], grid[row][col]



def draw_grid() -> None:
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] != 0: 
                draw_cell(row, col)

    
def draw_cell(row: int, col: int) -> None:
    rect = pygame.Rect(col * COL_SIZE, row * ROW_SIZE, COL_SIZE, ROW_SIZE)
    sand_color.hsva = (grid[row][col], 100, 100, 100)
    pygame.draw.rect(screen, sand_color, rect)


WIDTH = 600
HEIGHT = 600
ROWS = 100
COLS = 100
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
        grid[event_row][event_col] = int(hue)

        hue += 0.1
        if hue > 360: hue = 1

    update_grid()
    draw_grid()

    pygame.display.update()
    clock.tick(60)

pygame.quit()