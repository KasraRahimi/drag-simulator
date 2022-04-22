
import pygame
pygame.init()
font = pygame.font.SysFont("Georgia", 24)

WIDTH, HEIGTH = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption('Drag Simulator')

class Ship:
    scale = 1 / 1000
    drag = 1e-5
    timestep = 1

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
        answer = (dx**2 + dy**2)**(1/2)
        return answer

    def ignite(self, direction):
        """This method thrusts the ship in the direction
        that is in its parameters. The directions are: w, a, s, d"""
        if direction == 'w':
            self.ddy -= self.thrust * self.timestep
        if direction == 'a':
            self.ddx -= self.thrust * self.timestep
        if direction == 's':
            self.ddy += self.thrust * self.timestep
        if direction == 'd':
            self.ddx += self.thrust * self.timestep

    def resistance(self, is_on=True):
        if is_on and self.speed > 0:
            speed = self.speed
            dx, dy = self.dx, self.dy
            drag = speed**2 * self.drag
            self.ddx -= drag * (dx / speed) * self.timestep
            self.ddy -= drag * (dy / speed) * self.timestep
    
    def updateSpeed(self):
        self.dx += self.ddx * self.timestep
        self.dy += self.ddy * self.timestep
        self.ddx, self.ddy = 0, 0
    
    def displayInfo(self):
        speed = self.speed
        thrust = self.thrust
        text = f"Speed: {speed:.3f} m/s | Thrust: {thrust}"
        display = font.render(text, False, (200, 200, 200))
        screen.blit(display, (10, 10))

    def updatePosition(self):
        self.x += self.dx * self.timestep
        self.y += self.dy * self.timestep

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
        
        # these off set the x, y so that (0, 0)
        # becomes the center of the screen
        x = self.x * self.scale + WIDTH / 2
        y = self.y * self.scale + HEIGTH / 2
        pygame.draw.circle(screen, self.color, (x, y), 10)


def main():
    is_running = True
    clock = pygame.time.Clock()
    craft = Ship(500, (230, 0, 30))

    while is_running:
        clock.tick(120)
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
        if keys[pygame.K_DOWN]:
            craft.thrust -= 10 if craft.thrust > 0 else 0
        if keys[pygame.K_UP]:
            craft.thrust += 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        
        craft.resistance()
        craft.updateSpeed()
        craft.updatePosition()
        craft.draw()
        craft.displayInfo()

        pygame.display.update()

        

if __name__ == "__main__":
    main()