
import pygame

WIDTH, HEIGTH = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption('Drag Simulator')

class Ship:
    scale = 1 / 100
    drag = 0.00001

    def __init__(self, thrust=10, color=(0, 0, 0)):
        self.thrust = thrust
        self.color = color
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.ddx = 0
        self.ddy = 0
    
    @property
    def speed(self):
        dx, dy = self.dx, self.dy
        return (dx**2 + dy**2)**(1/2)

    def ignite(self, direction):
        """This method thrusts the ship in the direction
        that is in its parameters. The directions are: w, a, s, d"""
        match direction:
            case 'w':
                self.ddy -= self.thrust
            case 'a':
                self.ddx -= self.thrust
            case 's':
                self.ddy += self.thrust
            case 'd':
                self.ddx += self.thrust

    def resistance(self, is_on=True):
        if is_on and self.speed > 0:
            speed = self.speed
            dx, dy = self.dx, self.dy
            drag = speed**2 * self.drag
            self.ddx -= drag * (dx / speed)
            self.ddy -= drag * (dy / speed)
    
    def updateSpeed(self):
        self.dx += self.ddx
        self.dy += self.ddy
        self.ddx, self.ddy = 0, 0

    def updatePosition(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        
        # these if statements allow the ship to warp around
        # if it hits on of the the screen borders
        if self.x < -WIDTH / (2 * self.scale):
            self.x = WIDTH / (2 * self.scale)
        elif self.x > WIDTH / (2 * self.scale):
            self.x = -WIDTH / (2 * self.scale)
        if self.y < -HEIGTH / (2 * self.scale):
            self.y = HEIGTH / (2 * self.scale)
        elif self.y > HEIGTH / (2 * self.scale):
            self.y = -HEIGTH / (2 * self.scale)
        
        x = self.x * self.scale + WIDTH / 2
        y = self.y * self.scale + HEIGTH / 2
        pygame.draw.circle(screen, self.color, (x, y), 10)


def main():
    is_running = True
    clock = pygame.time.Clock()
    craft = Ship(500, (230, 0, 30))

    while is_running:
        clock.tick(30)
        screen.fill((0, 0, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            craft.ignite('w')
        if keys[pygame.K_a]:
            craft.ignite('a')
        if keys[pygame.K_s]:
            craft.ignite('s')
        if keys[pygame.K_d]:
            craft.ignite('d')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        
        craft.resistance()
        craft.updateSpeed()
        craft.updatePosition()
        craft.draw()

        pygame.display.update()

        

if __name__ == "__main__":
    main()