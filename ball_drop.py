import pygame
import math
pygame.init()
pygame.mixer.init()

sound = pygame.mixer.Sound("/Users/everettwhidden/Documents/sounds_python/mixkit-basketball-ball-hard-hit-2093.wav")



width, height = (800,800)
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball Drop Simulation")
x_values = [45, 125, 205, 285, 365, 445, 525, 605, 685]
planets = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']



G = 6.674e-11
class Planet:
    global G
    def __init__(self, mass, radius):
        self.gravity = G * mass / radius**2

sun = Planet(1.989e30, 6.957e8)
mercury = Planet(3.285e23, 2.439e6)
venus = Planet(4.867e24, 6.051e6)
earth = Planet(5.972e24, 6.371e6)
mars = Planet(6.39e23, 3.389e6)
jupiter = Planet(1.898e27, 6.991e7)
saturn = Planet(5.683e26, 5.823e7)
uranus = Planet(8.681e25, 2.536e7)
neptune = Planet(1.024e26, 2.462e7)

planet_obj= {
    "Sun" : sun,
    "Mercury" : mercury,
    "Venus" : venus,
    "Earth" : earth,
    "Mars" : mars,
    "Jupiter" : jupiter,
    "Saturn" : saturn,
    "Uranus" : uranus,
    "Neptune" : neptune,
}

class Ball:
    timestep = 1/60
    scale = 200 # 1 meter is 200 pixels
    
    def __init__(self, height, planet_on):
        self.y_vel = 0
        self.height = height
        self.x = 400
        self.y = 680 - height * self.scale
        self.planet = planet_on
        self.bouncing = False
        

    def drop(self):
        
        self.y_vel += self.planet.gravity * (self.timestep) #vf = vi + a * dt
        self.y += self.y_vel * self.timestep * self.scale #updating position 

        if self.y > 655:
            self.y = 655
            self.y_vel = -self.y_vel * 0.85
            if abs(self.y_vel) <= 0.15:
                self.y_vel = 0
                self.y = 655
            elif not self.bouncing:
                sound.play()
                self.bouncing = True
        else:
            self.bouncing = False


            #self.y_vel = 0

        

    def draw(self, win):
        global x_values
        global planets 
        font = pygame.font.SysFont("arial", 14)
        pygame.draw.circle(win, (204, 111, 20), (self.x, self.y) , 25)
        pygame.draw.line(win, (255, 255, 255), (0, 680), (800, 680), 2) #Floor
        for x in x_values:
            pygame.draw.rect(win, (255, 255, 255), (x, 25, 80, 30))

        for i, x in enumerate(x_values):
            text = font.render(planets[i], True, (0,0,0))
            text_rect = text.get_rect(center=(x + 40, 40))  # 40 = half rect width, 40 = rect y + half height
            win.blit(text, text_rect)






def main():
    run = True
    clock = pygame.time.Clock()
    ball = Ball(3, earth)
    
    
    

    while run:
        clock.tick(60)
        win.fill((0,0,0))
        global x_values
        global planets 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                ball.y = 680 - ball.height * ball.scale
                ball.y_vel = 0
                for i, x in enumerate(x_values):
                    if pygame.Rect(x, 25, 80, 30).collidepoint(event.pos):
                        ball.planet = planet_obj[planets[i]]
        ball.drop()
        ball.draw(win)

        pygame.display.update()
    
    pygame.quit()

main()