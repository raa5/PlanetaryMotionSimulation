import pygame
import math

# Init pygame application
pygame.init()

# Set Pygame window width and height
WIDTH, HEIGHT = 800, 800
# Set display screen's width and height
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Set title of window
pygame.display.set_caption('Planet Simulation')

# Define a window color and other colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16, bold= True)

# Implementing Planets
class Planet:

    # Defining 1 Astronomical Unit in meters
    AU = 149.6e6 * 1000
    # Define Gravitational constant
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day


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
        # Since we need to draw to scale and also to be positioned in the center of the window
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                updated_points.append((x, y))

            pygame.draw.lines(WIN, self.color, False, updated_points, 2)


        # Drawing circle in the center of the screen
        pygame.draw.circle(win, color=self.color, center=(x,y), radius=self.radius)
        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", True, WHITE)
            WIN.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

    # Defining function for attraction forces
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2) 

        # To append to distance to sun list
        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    # Defining function to update position
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Computing velocities
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Computing positions
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))



# Main function to keep pygame loop running
def main():
    run = True
    # Adding clock so that frame rate of our game doesnt go over a certain value
    clock = pygame.time.Clock()

    # Initializing planets (and stars)
    sun = Planet(0, 0, 30, YELLOW, 1.98892*10**30)
    sun.sun = True

    # Initializing Earth
    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742*10**24)
    earth.y_vel = 29.783 * 1000

    # Initializing Mars
    mars = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39*10**23)
    mars.y_vel = 24.077 * 1000

    # Initializing Mercury
    mercury = Planet(0.387*Planet.AU, 0, 8, DARK_GREY, 0.33*10**24)
    mercury.y_vel = -47.4 * 1000
    
    # Initializing Venus
    venus = Planet(0.723*Planet.AU, 0, 14, WHITE, 4.8685*10**24)
    venus.y_vel = -35.02 * 1000
    
    planets = [sun, earth, mars, mercury, venus]

    while run:
        # Indicate how many max uframe updates per second
        clock.tick(60)
        # Set window fill color
        WIN.fill((0,0,0))
        # # Without this the window background color won't actually change to white
        # pygame.display.update()
        for event in pygame.event.get():
            # User can only control closing the window by pressing the X button
            if event.type == pygame.QUIT:
                # End pygame simulation
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()
