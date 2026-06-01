import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
TAN = (230, 228, 188)

earth_days = 0
mars_days = 0 
mercury_days = 0
venus_days = 0

FONT = pygame.font.SysFont("consolas", 20,)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 100 / AU # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24 # 1 day
  
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0


    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
    
        if len(self.orbit) >= 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)
    
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2 - 25))
    
        
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy, = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append([self.x, self.y])


def main():
    run = True
    clock = pygame.time.Clock()
    global earth_days
    global venus_days
    global mars_days
    global mercury_days
    

    slider_x = 20
    slider_y = HEIGHT - 40
    slider_width = 200
    slider_min = 1
    slider_max = 10
    slider_val = 1
    dragging = False

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.007 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(5.2 * Planet.AU, 0, 21, TAN, 1.898 * 10**27)
    jupiter.y_vel = -13.07 * 1000

    saturn = Planet(9.58 * Planet.AU, 0, 18, TAN, 5.683 * 10**26)
    saturn.y_vel = -9.69 * 1000




    planets = [sun, earth, mars, mercury, venus, jupiter, saturn] #jupiter, #saturn]
    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        earth_days += 1
        mars_days += 1 / 1.027
        venus_days += 1 / 243
        mercury_days += 1 / 58.6
        mx = 0
        my = 0

        substeps = int(slider_val)
        for _ in range(substeps):
            for planet in planets:
                planet.update_position(planets)
                planet.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
    
                if slider_y - 10 < my < slider_y + 10 and slider_x < mx < slider_x + slider_width:
                    dragging = True

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                mx, my = pygame.mouse.get_pos()
                slider_val = round((mx - slider_x) / slider_width * slider_max, 2)
                slider_val = max(slider_min, min(slider_max, slider_val))

        pygame.draw.rect(WIN, DARK_GREY, (slider_x, slider_y, slider_width, 4))
        handle_x = int(slider_x + (slider_val / slider_max) * slider_width)
        pygame.draw.circle(WIN, WHITE, (handle_x, slider_y), 8)
        speed_text = FONT.render(f"Speed: {slider_val}x", 1, WHITE)
        WIN.blit(speed_text, (slider_x, slider_y - 25))
        
       

        earth_day_text = FONT.render(f"Number of Earth days passed: {earth_days}", 1, WHITE) 
        WIN.blit(earth_day_text, (20,20))
        venus_day_text = FONT.render(f"Number of Venus days passed: {round(venus_days, 1)}", 1, WHITE) 
        WIN.blit(venus_day_text, (20,40))
        mars_day_text = FONT.render(f"Number of Mars days passed: {round(mars_days)}", 1, WHITE) 
        WIN.blit(mars_day_text, (20,60))
        mercury_day_text = FONT.render(f"Number of Mercury days passed: {round(mercury_days, 1)}", 1, WHITE) 
        WIN.blit(mercury_day_text, (20,80))


        pygame.display.update()
    
    pygame.quit()

main()