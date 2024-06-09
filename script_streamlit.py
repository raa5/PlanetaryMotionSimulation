import math
import matplotlib.pyplot as plt
import streamlit as st

# Define colors for plotting
YELLOW = 'yellow'
BLUE = 'blue'
RED = 'red'
DARK_GREY = 'grey'
WHITE = 'white'

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

def main():
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

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    ax.set_xlim(-2*Planet.AU, 2*Planet.AU)
    ax.set_ylim(-2*Planet.AU, 2*Planet.AU)

    for _ in range(365):  # Simulate for one year
        for planet in planets:
            planet.update_position(planets)
            x, y = zip(*planet.orbit)
            ax.plot(x, y, color=planet.color)
            ax.scatter(planet.x, planet.y, color=planet.color, s=planet.radius)

    st.pyplot(fig)

if __name__ == "__main__":
    main()
