import pygame, math
import random

class Wall:
    def __init__(self, surface, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.surface = surface
    
    def draw(self):
        pygame.draw.line(self.surface, (255, 255, 255), (self.x1, self.y1), (self.x2, self.y2))


class Ray:
    def __init__(self, surface, x1, y1, theta):
        self.r = 1000
        self.x1 = x1
        self.y1 = y1
        self.x2 = self.x1 + self.r * math.cos(theta)
        self.y2 = self.y1 + self.r * math.sin(theta)
        self.surface = surface
    
    def draw(self):
        # pygame.draw.circle(self.surface, (25, 100, 200), (self.x1, self.y1), 5)
        pygame.draw.line(self.surface, (255, 255, 255), (self.x1, self.y1), (self.x2, self.y2))

    def cast(self, wall):
        x1 = wall.x1
        y1 = wall.y1
        x2 = wall.x2
        y2 = wall.y2

        x3 = self.x1
        y3 = self.y1
        x4 = self.x2
        y4 = self.y2

        try:
            t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4))/((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
            u = ((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3))/((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
            if (0 <= t and t <= 1) and u < 0:
                px = round(x1 + t*(x2 - x1))
                py = round(y1 + t*(y2 - y1))
                # pygame.draw.circle(self.surface, (255, 255, 255), (px, py), 3)
                # self.x2 = px
                # self.y2 = py
                return [px, py]
        except ZeroDivisionError:
            pass

        return [-1, -1]

class Player:
    def __init__(self, surface, x1, y1, walls):
        self.x1 = x1
        self.y1 = y1
        self.surface = surface
        self.walls = walls

    def draw(self):
        pygame.draw.circle(self.surface, (25, 100, 200), (self.x1, self.y1), 5)
        for i in range(360):
            if i % 2 == 0:
                r = Ray(self.surface, self.x1, self.y1, math.radians(i))
                min_dist = 1000
                min_pt = [-1, -1]
                for j in range(len(self.walls)):
                    [px, py] = r.cast(self.walls[j])
                    d = abs(self.x1 - px) + abs(self.y1 - py)
                    if d < min_dist:
                        min_dist = d
                        min_pt = [px, py]

                # pygame.draw.circle(self.surface, (255, 255, 255), (min_pt[0], min_pt[1]), 5)
                if min_pt[0] != -1:
                    r.x2 = min_pt[0]
                    r.y2 = min_pt[1]
                r.draw()


def maze_generator(n, disp):
    # Generate random walls
    walls = []
    for i in range(n):
        walls.append(Wall(disp, random.randrange(20, 800), random.randrange(20, 600), random.randrange(20, 800), random.randrange(20, 600)))
    return walls

pygame.init()

disp = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Raycaster")

clock = pygame.time.Clock()

crashed = False

# w1 = Wall(disp, 400, 540, 50, 200)
# w2 = Wall(disp, 100, 150, 400, 300)
# walls = [w1, w2]
r = Ray(disp, 100, 100, math.radians(-45))
walls = maze_generator(5, disp)
p = Player(disp, 100, 100, walls)
while not crashed:
    disp.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        
        p.x1 = pygame.mouse.get_pos()[0]
        p.y1 = pygame.mouse.get_pos()[1]

        # print(event)
    for i in range(len(walls)):
        walls[i].draw()
    # r.draw()
    p.draw()
    # r.cast(w1)
    # r.cast(w2)

    pygame.display.update()
    clock.tick(60)