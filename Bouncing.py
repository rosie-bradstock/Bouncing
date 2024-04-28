import pygame
import random
import math

WIDTH = 700
HEIGHT = 700
FPS = 50

class Ball(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        # make the image
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image, (255,255,255), (25,25), 25)
        self.rect = self.image.get_rect()

        # define important attributes
        self.movement = (self.make_random_movement())
        self.position = position
        self.held = False
        self.to_mouse = False

    # makes a random starting movement for the ball
    def make_random_movement(self):
        i = random.randint(1,1000)
        j = 1000 - i
        x = random.randint(1,4)
        if x == 1:
            i *= -1
            j *= -1
        elif x == 2:
            i *= -1
        elif x == 3:
            j *= -1
        return(i//200,j//200)
        
    def set_movement(self, new):
        self.movement = new

    def set_position(self, new):
        self.position = new

    def get_movement(self):
        return self.movement

    def get_rect(self):
        return self.rect

    def get_position(self):
        return self.position

    def set_held(self, value):
       self.held = value

    def get_held(self):
        return self.held
    
    def get_to_mouse(self):
        return self.to_mouse
    
    def set_to_mouse(self, new):
        self.to_mouse = new

    # moves the ball to its new position
    def move(self):
        self.position = (int(self.position[0] + self.movement[0]), int(self.position[1] + self.movement[1]))
        self.rect.center = self.position

        if self.rect.right >= WIDTH * 0.99:
            self.rect.right = WIDTH
        if self.rect.left <= WIDTH * 0.01:
            self.rect.left = 0
        if self.rect.top <= HEIGHT * 0.01:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT * 0.99:
            self.rect.bottom = HEIGHT

    # lets the ball pass through the edges of the screen
    def check_edges_pass_through(self):
        if self.rect.center[0] > WIDTH:
            self.position = (0,self.position[1])
        elif self.rect.center[0] < 0:
            self.position = (WIDTH, self.position[1])

        if self.rect.center[1] > HEIGHT:
            self.position = (self.position[0], 0)
        elif self.rect.center[1] < 0:
            self.position = (self.position[0], WIDTH)

    # lets the ball bounce off the edges of the screen
    def check_edges_bounce(self):
        if self.rect.right >= WIDTH * 0.99:
            self.movement = (self.movement[0] * -0.99 + WIDTH * 0.001, self.movement[1])
            pygame.mixer.Sound.play(random.choice((bounce_1, bounce_2, bounce_3, bounce_4)))
        if self.rect.left <= WIDTH * 0.01:
            self.movement = (self.movement[0] * -0.99 + WIDTH * 0.001, self.movement[1])
            pygame.mixer.Sound.play(random.choice((bounce_1, bounce_2, bounce_3, bounce_4)))
        if self.rect.top <= HEIGHT * 0.01:
            self.movement = (self.movement[0], self.movement[1] * -0.9 + HEIGHT * 0.01)
            pygame.mixer.Sound.play(random.choice((bounce_1, bounce_2, bounce_3, bounce_4)))
        if self.rect.bottom >= HEIGHT * 0.99:
            self.movement = (self.movement[0], self.movement [1] * -0.9 + HEIGHT * 0.01)
            pygame.mixer.Sound.play(random.choice((bounce_1, bounce_2, bounce_3, bounce_4)))

    def update(self):
        if self.held:
            self.rect.center = (pygame.mouse.get_pos())
        elif abs(int(self.movement[1])) <= 5 and abs(int(self.movement[0])) <= 5 and self.rect.bottom >= (HEIGHT * 0.99):
            self.movement = (0,0)
            self.rect.bottom = HEIGHT
        else:
            self.check_edges_bounce()
            self.move()
            # add gravity
            self.movement = (self.movement[0] * 0.995, (self.movement[1]) + (check_magnitude(self.movement) * 0.3) + 0.1)

# set up the screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# define the sounds
bounce_1 = pygame.mixer.Sound("bounce_1.mp3")
bounce_2 = pygame.mixer.Sound("bounce_2.mp3")
bounce_3 = pygame.mixer.Sound("bounce_3.mp3")
bounce_4 = pygame.mixer.Sound("bounce_4.mp3")

# makes the ball
ball = Ball((WIDTH // 2, HEIGHT // 2))
all_sprites.add(ball)

# adds an unlimited number of vectors
def add_vectors(*args):
    i = 0
    j = 0
    for v in args:
        i = i + v[0]
        j = j + v[1]
    return (i,j)

# finds the hyp
def check_magnitude(vect):
    return math.sqrt(vect[0]**2 + vect[1]**2)
    
# game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ball.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0] == True:
                    ball.set_held(True)
                    start_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[2] == True:
                ball.set_to_mouse(True)
        elif event.type == pygame.MOUSEBUTTONUP:
            if ball.get_held():
                ball.set_held(False)
                end_pos = pygame.mouse.get_pos()
                new_movement = ((end_pos[0] - start_pos[0])/10, (end_pos[1] - start_pos[1])/10)
                ball.set_position(end_pos)
                ball.set_movement(new_movement)
            ball.set_to_mouse(False)
                
    if ball.get_to_mouse():
        new_movement = ((pygame.mouse.get_pos()[0] - ball.get_position()[0]) /5, (pygame.mouse.get_pos()[1] - ball.get_position()[1])/5)
        ball.set_movement(new_movement)

    screen.fill((0,0,0))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
