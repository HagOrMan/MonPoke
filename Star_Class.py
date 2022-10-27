import pygame


# Makes a list of all the png file names for all pokemon.
def make_star_list():
    star_list = []
    pokemon = ['caught_star']
    distances = ['close', 'medium', 'far']

    # Makes a list of all the pokemon and all their distances as the name of their png files.
    for poke in pokemon:
        for dist in distances:
            star_list.append(poke + '_' + dist + '.png')

    return star_list


class StarGroup:

    def __init__(self, ball):
        self.radius = 5
        self.image = pygame.image.load('caught_star_far.png')
        self.star_list = make_star_list()
        self.x, self.y = self.decide_pos(ball)
        self.visible = True

    # Decides the starting position and size of the star based on whether the ball is big, medium, or small.
    def decide_pos(self, ball):
        radius = ball.get_radius()
        ball_x = ball.get_x_pos()
        ball_y = ball.get_y_pos()

        # Sets the size of the star based on how small/big the ball is.
        if radius <= 15:
            self.radius = 5
            self.image = pygame.image.load(self.star_list[2])
        elif radius > 22.5:
            self.radius = 10
            self.image = pygame.image.load(self.star_list[0])
        else:
            self.radius = 7.5
            self.image = pygame.image.load(self.star_list[1])

        x = ball_x - self.radius
        y = ball_y - radius - self.radius

        return x, y

    # Draws the 3 stars above the ball.
    def draw_self(self, win):
        if self.visible:
            win.blit(self.image, (self.x, self.y))
            win.blit(self.image, (self.x + self.radius * 2.5, self.y + self.radius / 5))
            win.blit(self.image, (self.x - self.radius * 2.5, self.y + self.radius / 5))

    # Setters

    # Sets the position of the stars based on the ball.
    def set_pos(self, ball):
        self.x, self.y = self.decide_pos(ball)

    def set_visible(self, visibility):
        self.visible = visibility

    # Getters
    def get_pos(self):
        return self.x. self.y
