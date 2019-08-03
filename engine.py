import pygame, math

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
        self.x1 = x1
        self.y1 = y1
        self.x2 = 100*math.cos(theta)
        self.y2 = 100*math.sin(theta)
        self.surface = surface
    
    def draw(self):
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
                pygame.draw.circle(self.surface, (255, 255, 255), (px, py), 3)
        except ZeroDivisionError:
            pass
       

pygame.init()

disp = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Raycaster")

clock = pygame.time.Clock()

crashed = False

w1 = Wall(disp, 50, 50, 300, 70)
w2 = Wall(disp, 100, 150, 400, 300)
r = Ray(disp, 100, 100, math.radians(45))

while not crashed:
    disp.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        
        # r.x2 = pygame.mouse.get_pos()[0]
        # r.y2 = pygame.mouse.get_pos()[1]

        # print(event)
    w1.draw()
    w2.draw()
    r.draw()

    r.cast(w1)
    r.cast(w2)

    pygame.display.update()
    clock.tick(60)