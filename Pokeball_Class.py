import pygame
import math


# Draws whether it was a nice, great, or excellent throw on the screen.
def draw_catch_msg(win, x, y, caught_text):

    word_font = pygame.font.Font("freesansbold.ttf", 20)
    caught_msg = word_font.render(caught_text, False, (255, 255, 255))
    win.blit(caught_msg, (x, y))


class Pokeball:

    def __init__(self, radius, x, y):
        self.radius = radius
        self.x = x
        self.y = y
        self.min_radius = 15
        self.speed_y = 0
        self.speed_x = 0

    # Adds the specified x and y values to the coordinate value of the ball.
    def move_ball(self, x, y):
        self.x += x
        self.y += y

    # Sets the position of the ball.
    def set_pos(self, x, y):
        self.x = x
        self.y = y

    # Changes the radius of the ball
    def change_radius(self, radius):
        self.radius = radius

    def get_radius(self):
        return self.radius

    def get_x_pos(self):
        return self.x

    def get_y_pos(self):
        return self.y

    def draw_ball(self, win, Color, catching):
        pygame.draw.circle(win, Color["lightRed"], [self.x, self.y], self.radius)
        pygame.draw.circle(win, (255, 255, 255), [self.x, self.y], self.radius, 0, False, False, True, True)
        pygame.draw.circle(win, (0, 0, 0), [self.x, self.y], self.radius / 2.2)
        pygame.draw.circle(win, (240, 240, 240), [self.x, self.y], self.radius / 2.7)
        pygame.draw.line(win, (0, 0, 0), (self.x - self.radius, self.y), (self.x + self.radius, self.y), int(self.radius / 5))
        pygame.draw.circle(win, (0, 0, 0), [self.x, self.y], self.radius / 3.3)

        # Draws white inner ball if not catching, and red if catching.
        if not catching:
            pygame.draw.circle(win, (255, 255, 255), [self.x, self.y], self.radius / 4)
        else:
            pygame.draw.circle(win, (255, 50, 50), [self.x, self.y], self.radius / 4)

    def throw_ball(self, win, Color, clock, speed, win_background, angle, pokemon, poke_caught, catch_circle):
        v1x = -speed * math.cos(angle)
        v1y = speed * math.sin(angle)
        self.speed_x = v1x
        time = 0
        t = 60/1000
        v2y = v1y
        g = -9.81

        # Total time in air is 3/4 of the normal so that it goes up to the vertex and then slightly down.
        total_time = (-1 * v1y * 2 / g) * (4 / 5)

        while time < total_time:

            self.move_ball(v1x, -v2y)
            v2y = v1y + g * t
            v1y = v2y

            if self.radius > self.min_radius:
                self.radius -= 0.35

            # win.fill(winColor)
            win.blit(win_background, (0, 0))

            pokemon.draw_self(win)
            catch_circle.draw_circle(win)
            self.draw_ball(win, Color, poke_caught)

            pygame.display.flip()

            time += t
            if time < total_time:
                self.speed_y = v1y
            clock.tick(60)

    # Has the ball keep bouncing past the pokemon.
    def bounce_past(self, win, Color, win_background, pokemon, clock, poke_caught, catch_circle):

        # Makes the speeds a bit lower than the original speed from the throw.
        v1x = self.speed_x
        v1y = -self.speed_y / 1.3

        time = 0
        t = 60 / 1000
        v2y = v1y
        g = -9.81

        # Total time in air is 9/10 of the normal so that it goes up to the vertex and then slightly down.
        total_time = (-1 * v1y * 2 / g) * (9 / 10)

        while time < total_time:

            self.move_ball(v1x, -v2y)
            v2y = v1y + g * t
            v1y = v2y

            if self.radius > self.min_radius:
                self.radius -= 0.35

            # win.fill(winColor)
            win.blit(win_background, (0, 0))

            pokemon.draw_self(win)
            catch_circle.draw_circle(win)
            self.draw_ball(win, Color, poke_caught)

            pygame.display.flip()

            time += t
            if time < total_time:
                self.speed_y = v1y
            clock.tick(60)

    # Has the ball bounce off of a pokemon after it has landed within the pokemon's radius.
    def bounce_off(self, win, Color, win_background, pokemon, clock, poke_caught, catch_circle):

        # Checks if the pokeball is within the catch circle and if it was a nice, great, or excellent throw.
        in_circle, good_catch = catch_circle.within(self.x, self.y, self.radius)
        x, y = catch_circle.get_x_pos(), catch_circle.get_y_pos()

        # Sets the caught message depending on the type of catch it was.
        if good_catch == 1:
            caught_msg = 'Nice!'
        elif good_catch == 2:
            caught_msg = 'Great!'
        else:
            caught_msg = 'Excellent'

        v1y = -self.speed_y / 1.5

        # If the velocity is not high enough to be noticeable, makes it noticeable.
        if v1y < 5:
            v1y = 5

        v2y = v1y

        time = 0
        t = 60 / 1000
        v2y = v1y
        g = -9.81

        # Goes up at least until velocity is negative.
        while v1y > 0:
            self.move_ball(0, -v2y)
            v2y = v1y + g * t
            v1y = v2y

            # win.fill(winColor)
            win.blit(win_background, (0, 0))

            pokemon.draw_self(win)
            if in_circle:
                draw_catch_msg(win, x, y, caught_msg)
            self.draw_ball(win, Color, poke_caught)

            pygame.display.flip()

            time += t
            clock.tick(60)

        # Keeps going down until the ball is at ground level for the pokemon.
        while self.y < pokemon.get_pos()[1] + 2 * pokemon.get_radius() - self.radius:

            self.move_ball(0, -v2y)
            v2y = v1y + g * t
            v1y = v2y

            # win.fill(winColor)
            win.blit(win_background, (0, 0))

            pokemon.draw_self(win)
            if in_circle:
                draw_catch_msg(win, x, y, caught_msg)
            self.draw_ball(win, Color, poke_caught)

            pygame.display.flip()

            time += t
            clock.tick(60)

        return good_catch
