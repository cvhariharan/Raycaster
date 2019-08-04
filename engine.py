import pygame, math
import random

class World:
    def __init__(self, surface, startfov, endfov, W, H):
        self.surface = surface
        fov = endfov - startfov
        self.rectwidth = int(W/fov)
        self.W = W
        self.H = H

    def mapFromTo(self, x, a, b, c, d):
        y=(x-a)/(b-a)*(d-c)+c
        return y

    def update(self, world):
        self.world = world
        for i in range(len(world)):
            b = self.mapFromTo(world[i], 0, 1000, 40, 255)
            h = self.mapFromTo(world[i], 0, 1000, 10, self.H)
            pygame.draw.rect(self.surface, (0, 0, 255-b), (i*self.rectwidth, abs(self.H/2 - h/2), self.rectwidth, self.H - h))

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
        self.px = 1000
        self.py = 1000
    
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
                self.px = round(x1 + t*(x2 - x1))
                self.py = round(y1 + t*(y2 - y1))
                
                return [self.px, self.py]
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
        W = 800
        H = 600

        startfov = -115
        endfov = -65
        fov = endfov - startfov
        rectwidth = int(W/fov)
        world = [1000]*fov
        renderer = World(self.surface, startfov, endfov, W, H)
        for i in range(startfov, endfov):
            world[i-startfov] = 1000
            # if i % 2 == 0:
            r = Ray(self.surface, self.x1, self.y1, math.radians(i))
            min_dist = 1000
            min_pt = [-1, -1]
            for j in range(len(self.walls)):
                [px, py] = r.cast(self.walls[j])
                d = ((self.x1 - px)**2 + (self.y1 - py)**2)**0.5
                if d < min_dist:
                    min_dist = d
                    min_pt = [px, py]


            if min_pt[0] != -1:
                r.x2 = min_pt[0]
                r.y2 = min_pt[1]
                world[i-startfov] = min_dist
                    
            renderer.update(world)


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

walls = maze_generator(5, disp)
p = Player(disp, 100, 100, walls)
while not crashed:
    disp.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        
        # p.x1 = pygame.mouse.get_pos()[0]
        # p.y1 = pygame.mouse.get_pos()[1]
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LEFT]:
        p.x1 -= 8

    if keys_pressed[pygame.K_RIGHT]:
        p.x1 += 8

    if keys_pressed[pygame.K_UP]:
        p.y1 -= 16

    if keys_pressed[pygame.K_DOWN]:
        p.y1 += 16

        # print(event)
    # for i in range(len(walls)):
    #     walls[i].draw()
    # r.draw()
    p.draw()
    # r.cast(w1)
    # r.cast(w2)

    pygame.display.update()
    clock.tick(60)