import pygame


class Bird:
    def __init__(self, screen_width, screen_height, net):
        self.screen_height = screen_height
        self.y = int(screen_height / 2)
        self.x = int(screen_width / 2)
        self.net = net

        self.score = 0
        self.alive = True

        self.width, self.height = 50, 50

    def move(self, pipe_y):
        output = self.net.activate(
            (
                self.y,
                abs(self.y - pipe_y[0]),
                abs(self.y - (self.screen_height - pipe_y[1])),
            )
        )

        jump = output[0] > output[1]

        if jump:
            if self.y - 5 > 0:
                self.y -= 5
            else:
                return True
        else:
            if self.y + 5 < self.screen_height:
                self.y += 5
            else:
                return True
        return False

    def draw(self, window):
        if self.alive:
            pygame.draw.rect(
                window, (255, 255, 255), (self.x, self.y, self.width, self.height)
            )
