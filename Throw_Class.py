import pygame
import math


class Thrower:

    def __init__(self, win_width, win_height, colour, length):
        self.x = win_width / 2
        self.y = win_height * 0.92
        self.angle = 90
        self.length = length
        self.end_point = 0
        self.colour = colour
        self.max_length = win_height / 5
        self.min_length = 20
        self.tip_length = self.length / 4
        self.tip_angle = 30
        self.tip_end1 = (0.0, 0.0)
        self.tip_end2 = (0.0, 0.0)
        self.__visible = True

        self.calc_endpoint()

        # Makes sure that the thrower isn't too big or small
        if self.length > self.max_length:
            self.length = self.max_length
        if self.length < self.min_length:
            self.length = self.min_length

    # Resets the throw line to how it started.
    def reset_throw(self):
        self.length = self.max_length / 2
        self.angle = 90
        self.calc_endpoint()

    # Draws the line showing where the player is aiming.
    def draw_throw(self, win):
        if not self.__visible:
            return
        pygame.draw.line(win, self.colour, (self.x, self.y), self.end_point, 3)

        # Draws the tip of the arrow
        pygame.draw.line(win, self.colour, self.end_point, self.tip_end1, 3)
        pygame.draw.line(win, self.colour, self.end_point, self.tip_end2, 3)

    # Calculates the new angle that the thrower should be at
    def change_angle(self, angle_change):
        if not self.__visible:
            return

        if self.angle + angle_change < 0:
            self.angle = 0
        elif self.angle + angle_change > 180:
            self.angle = 180
        else:
            self.angle += angle_change
        self.calc_endpoint()

    # Calculates the endpoint based on the angle that the throw is made at.
    def calc_endpoint(self):
        # Endpoint for line.
        self.end_point = (self.x - math.cos(self.angle * math.pi / 180) * self.length,
                          self.y - math.sin(self.angle * math.pi / 180) * self.length)

        # Endpoint for tips of arrow
        self.tip_end1 = (self.end_point[0] + math.cos((self.angle + self.tip_angle) * math.pi / 180) * self.tip_length,
                         self.end_point[1] + math.sin((self.angle + self.tip_angle) * math.pi / 180) * self.tip_length)
        self.tip_end2 = (self.end_point[0] + math.cos((self.angle - self.tip_angle) * math.pi / 180) * self.tip_length,
                         self.end_point[1] + math.sin((self.angle - self.tip_angle) * math.pi / 180) * self.tip_length)

    # Changes the length / power of the throw
    def change_length(self, length_change):
        if not self.__visible:
            return

        self.length += length_change
        if self.length > self.max_length:
            self.length = self.max_length
        if self.length < self.min_length:
            self.length = self.min_length
        self.calc_endpoint()

    # Getters
    def get_length(self):
        return self.length

    def get_angle(self):
        return self.angle

    def get_visibility(self):
        return self.__visible

    # Setters
    def change_visible(self, visible):
        self.__visible = visible
