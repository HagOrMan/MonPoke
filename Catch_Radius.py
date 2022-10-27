import pygame
import math

Colour = {
    "white": (255, 255, 255),
    "light_green": (87, 253, 104),
    "green": (28, 230, 48),
    "yellow": (244, 250, 70),
    "orange": (255, 164, 60),
    "red": (255, 46, 46),
}


# Decides the radius of the circle depending on the difficulty of the catch.
def decide_radius(size: int):
    if size == 1:
        radius = 100
    elif size == 2:
        radius = 80
    elif size == 3:
        radius = 60
    elif size == 4:
        radius = 50
    else:
        radius = 40
    return radius


# Decides the colour of the circle depending on the difficulty of the catch.
def decide_colour(difficulty: int):
    if difficulty == 1:
        colour = Colour["light_green"]
    elif difficulty == 2:
        colour = Colour["green"]
    elif difficulty == 3:
        colour = Colour["yellow"]
    elif difficulty == 4:
        colour = Colour["orange"]
    else:
        colour = Colour["red"]
    return colour


# Decides the speed of the circle.
def decide_speed(speed: int):
    if speed == 1:
        return 0.15
    elif speed == 2:
        return 0.225
    else:
        return 0.3


class CatchRadius:
    def __init__(self, x: float, y: float, size: int, difficulty: int, speed: int):
        self.radius = decide_radius(size)
        self.max_radius = self.radius
        self.colour = decide_colour(difficulty)
        self.x = x
        self.y = y
        self.min_radius = 1
        self.speed = decide_speed(speed)
        self.visible = True

    # Sets the position of the ball.
    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_speed(self, speed):
        self.speed = decide_speed(speed)

    def set_visibility(self, visible: bool):
        self.visible = visible

    # Changes the radius of the ball
    def set_radius(self, size):
        self.radius = decide_radius(size)

    def set_colour(self, difficulty):
        self.colour = decide_colour(difficulty)

    def set_max_radius(self, radius):
        self.max_radius = radius

    def reset_radius(self):
        self.radius = self.max_radius

    # Decreases the radius by the decrease speed.
    def decrease_radius(self):
        self.radius -= self.speed

        # If decreasing it puts it lower than the min, resets it.
        if self.radius < self.min_radius:
            self.reset_radius()

    def get_radius(self):
        return self.radius

    def get_x_pos(self):
        return self.x

    def get_y_pos(self):
        return self.y

    def get_visibility(self):
        return self.visible

    # Draws the outer circle showing the max radius and draws the actual circle of the catch radius.
    def draw_circle(self, win):
        pygame.draw.circle(win, Colour["white"], [self.x, self.y], self.max_radius, 3)
        pygame.draw.circle(win, self.colour, [self.x, self.y], self.radius, 2)
        self.decrease_radius()

    # Checks if an object with a set radius and position is within the circle.
    # Returns whether the object is within, and then how small the circle is as either 1, 2, or 3. 1 is a 'Nice' Throw.
    # 0 means that it's not in.
    def within(self, x, y, radius):
        distance = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2) - radius

        if distance > self.radius:
            within = False
            return within, 0

        within = True

        # Returns if the circle is 1/3 of its max radius, 2/3, or more than 2/3.
        if self.radius <= self.max_radius / 3:
            return within, 3
        elif self.radius <= self.max_radius * 2 / 3:
            return within, 2
        else:
            return within, 1
