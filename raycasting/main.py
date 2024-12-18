import pygame
import random
import numpy as np

    
def dist(p1, p2) -> float:
    return np.sqrt(np.pow(p1[0] - p2[0], 2) + np.pow(p1[1] - p2[1], 2))


class Boundary:
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2


    def draw(self, screen) -> None:
        pygame.draw.line(surface=screen, 
                         color='red', 
                         start_pos=self.p1, 
                         end_pos=self.p2,
                         width=2)
        

class Ray:
    def __init__(self, pos, th: float) -> None:
        self.pos = pos
        self.th = th


    def move(self, pos) -> None:
        self.pos = pos


    def cast(self, boundary: Boundary) -> tuple[float, float]:
        # x = self.pos[0] + 5*math.cos(self.th)
        # y = self.pos[1] + 5*math.sin(self.th)
        # m = (y - self.pos[1])/(x - self.pos[0])
        # b = self.pos[1] - m * self.pos[0]

        # mb = (boundary.p1[1] - boundary.p2[1])/(boundary.p1[0] - boundary.p2[0])
        # bb = boundary.p1[1] - mb * boundary.p1[0]

        # x_inter = int((bb - b)/(m - mb))
        # y_inter = int(m * x_inter + b)

        # x_min, x_max = min(boundary.p1[0], boundary.p2[0]), max(boundary.p1[0], boundary.p2[0])
        # y_min, y_max = min(boundary.p1[1], boundary.p2[1]), max(boundary.p1[1], boundary.p2[1])
        # if x_min <= x_inter <= x_max and y_min <= y_inter <= y_max:
        #     return x_inter, y_inter
        # return None
    
        x1, y1 = self.pos
        x2 = x1 + np.cos(self.th)
        y2 = y1 + np.sin(self.th)
        x3, y3 = boundary.p1
        x4, y4 = boundary.p2

        den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
        if den == 0: return None
        t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / den
        u = -((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)) / den

        if t > 0 and 0 <= u <= 1:
            return (x3 + u*(x4 - x3), y3 + u*(y4 - y3))
        return None
    

class Raycaster:
    def __init__(self, pos) -> None:
        self.pos = pos
        self.rays = []
        for th in range(0, 360, 1):
            ray = Ray((self.pos[0], self.pos[1]), np.radians(th))
            self.rays.append(ray)

    
    def move(self, pos) -> None:
        self.pos = pos
        for ray in self.rays:
            ray.move(pos)

    
    def cast(self, boundaries: list[Boundary]) -> list[tuple[float, float]]:
        intersection_points = []
        for ray in self.rays:
            closest = None
            min_distance = float('inf')
            for boundary in boundaries:
                p = ray.cast(boundary)
                if not p: continue

                d = dist(self.pos, p)
                if d < min_distance:
                    min_distance = d
                    closest = p

            if closest: 
                intersection_points.append(closest)
        return intersection_points
        

WIDTH, HEIGHT = 500, 500
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

offset = WIDTH // 100
boundaries = [Boundary((offset, offset), (offset, HEIGHT-offset)),
              Boundary((offset, offset), (WIDTH-offset, offset)),
              Boundary((WIDTH-offset, offset), (WIDTH-offset, HEIGHT-offset)),
              Boundary((offset, HEIGHT-offset), (WIDTH-offset, HEIGHT-offset))]
for _ in range(5):
    b = Boundary((random.randint(0, WIDTH),
                  random.randint(0, HEIGHT)),
                 (random.randint(0, WIDTH),
                  random.randint(0, HEIGHT)))
    boundaries.append(b)

caster = Raycaster((WIDTH//2 , HEIGHT//2))
caster_ax, caster_ay = 0, 0
caster_vx, caster_vy = 0, 0

running = True
mouse_in_screen = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        if event.type == pygame.MOUSEMOTION:
            if (offset < event.pos[0] < WIDTH - offset) and (offset < event.pos[1] < HEIGHT - offset):
                mouse_in_screen = True
                caster.move(event.pos)
            else:
                mouse_in_screen = False

    if not mouse_in_screen:
        caster_ax = random.uniform(-0.3, 0.3)
        caster_ay = random.uniform(-0.3, 0.3)
        caster_vx += caster_ax
        caster_vy += caster_ay
        caster.move((np.clip(caster.pos[0] + caster_vx, offset, WIDTH-offset), 
                    np.clip(caster.pos[1] + caster_vy, offset, HEIGHT-offset)))
        caster_vx *= 0.99
        caster_vy *= 0.99
    else:
        caster_vx, caster_vy = 0, 0

    screen.fill('black')

    points = caster.cast(boundaries)
    for p in points:
        pygame.draw.line(screen, 'white', caster.pos, p)
    pygame.draw.circle(screen, 'red', caster.pos, 5)
    
    for b in boundaries: 
        b.draw(screen)

    pygame.display.update()
    clock.tick(60)
            
pygame.quit()