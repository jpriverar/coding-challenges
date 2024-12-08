import pygame
import random
import math

    
def dist(p1, p2) -> float:
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


class Boundary:
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2


    def draw(self, screen) -> None:
        pygame.draw.line(surface=screen, 
                         color='red', 
                         start_pos=self.p1, 
                         end_pos=self.p2,
                         width=1)
        

class Ray:
    def __init__(self, pos, th: float) -> None:
        self.pos = pos
        self.th = th


    def move(self, pos) -> None:
        self.pos = pos


    def cast(self, boundary: Boundary) -> tuple[float, float]:
        try: 
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
            x2 = x1 + math.cos(self.th)
            y2 = y1 + math.sin(self.th)
            x3, y3 = boundary.p1
            x4, y4 = boundary.p2

            den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
            t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / den
            u = -((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)) / den

            if 0 <= u <= 1:
                return x3 + u*(x4 - x3), y3 + u*(y4 - y3)
            return None
        except ZeroDivisionError as e:
            return None
    

class Raycaster:
    def __init__(self, pos) -> None:
        self.pos = pos
        self.rays = []
        for th in range(0, 180, 5):
            ray = Ray((self.pos[0], self.pos[1]), math.radians(th))
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

boundaries = [Boundary((10, 10), (10, HEIGHT-10)),
              Boundary((10, 10), (WIDTH-10, 10)),
              Boundary((WIDTH-10, 10), (WIDTH-10, HEIGHT-10)),
              Boundary((10, HEIGHT-10), (WIDTH-10, HEIGHT-10))]
for _ in range(5):
    b = Boundary((random.randint(0, WIDTH),
                  random.randint(0, HEIGHT)),
                 (random.randint(0, WIDTH),
                  random.randint(0, HEIGHT)))
    boundaries.append(b)

caster = Raycaster((WIDTH//2 , HEIGHT//2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        if event.type == pygame.MOUSEMOTION:
            caster.move(event.pos)

    screen.fill('black')
    for b in boundaries: b.draw(screen)

    pygame.draw.circle(screen, 'white', caster.pos, 5)
    points = caster.cast(boundaries)
    for p in points:
        pygame.draw.line(screen, 'white', caster.pos, p)
        #pygame.draw.circle(screen, 'red', p, 3)
    
    pygame.display.update()
    clock.tick(60)
            
pygame.quit()