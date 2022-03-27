import pygame
import math
pygame.init()

WIDTH, HEIGHT =  800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Colors Section
SUN = (255, 255, 0)
EARTH = (0, 0, 255)
MARS = (255, 0, 0)
VENUS = (165, 124, 27)
MERCURY = (80, 78, 81)
WHITE = (255, 255, 255)
JUPITER = (144, 97, 77)
SATURN = (195, 161, 113)
URANUS = (79, 208, 231)
NEPTUNE = (62, 84, 232)
PLUTO = (200, 233, 233)

# Font Section
FONT = pygame.font.SysFont("Comic Sans", 16)

class Planet:
	# Constants Declaration
	AU = 149.6e6 * 1000
	G = 6.67428e-11
	SCALE = 250/ AU  # 1AU = 100 pixels
	TIMESTEP = 3600*24 # 1 day

	# Attributes Declaration
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

	# To Draw Orbits
	def draw(self, win):
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2

		if len(self.orbit) > 2:
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
			win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

	
	# To Calculate Force Of Attraction
	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

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

		self.x_vel += total_fx / self.mass * self.TIMESTEP
		self.y_vel += total_fy / self.mass * self.TIMESTEP

		self.x += self.x_vel * self.TIMESTEP
		self.y += self.y_vel * self.TIMESTEP
		self.orbit.append((self.x, self.y))


def main():
	run = True
	clock = pygame.time.Clock()

	sun = Planet(0, 0, 30, SUN, 1.98892e30)
	sun.sun = True

	mercury = Planet(0.387 * Planet.AU, 0, 6.2, MERCURY, 3.30e23)
	mercury.y_vel = -47.4 * 1000
	
	venus = Planet(0.723 * Planet.AU, 0, 15, VENUS, 4.8685e24)
	venus.y_vel = -35.02 * 1000

	earth = Planet(-1 * Planet.AU, 0, 16, EARTH, 5.9742e24)
	earth.y_vel = 29.783 * 1000

	mars = Planet(-1.524 * Planet.AU, 0, 9, MARS, 6.39e23)
	mars.y_vel = 24.077 * 1000
	
	jupiter = Planet(5.203 * Planet.AU, 0 , 25, JUPITER, 1898.13e24)
	jupiter.y_vel = 13.06 * 1000

	saturn = Planet(9.537 * Planet.AU, 0 , 24, SATURN, 568.32e24)
	saturn.y_vel = 9.68 * 1000

	uranus = Planet(19.191 * Planet.AU, 0 , 20, URANUS, 86.811e24)
	uranus.y_vel = 6.80 * 1000

	neptune = Planet(30.608 * Planet.AU, 0, 19, NEPTUNE, 102.409e24)
	neptune.y_vel = 5.43 * 1000

	pluto = Planet(39.481 * Planet.AU, 0, 4.5, PLUTO, 1.303e22)
	pluto.y_vel = 4.67 * 1000

	planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]

	while run:
		clock.tick(60)
		WIN.fill((0, 0, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)

		pygame.display.update()

	pygame.quit()


main()