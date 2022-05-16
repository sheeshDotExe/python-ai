import pygame


class Pipe:
    def __init__(self, x, y1, y2):
        self.x, self.y1, self.y2 = x, y1, y2
        self.width = 50

    def move(self):
        if self.x - 2 > 0:
            self.x -= 2
            return False
        return True

    def draw(self, window, screen_height):
        pygame.draw.rect(window, (255, 0, 0), (self.x, 0, self.width, self.y1))

        pygame.draw.rect(
            window, (255, 0, 0), (self.x, screen_height - self.y2, self.width, self.y2)
        )

    def checkcollision(self, other, screen_height):
        if (
            self.x <= other.x + other.width
            and self.x + self.width > other.x + other.width
        ) or (self.x < other.x and self.x + self.width > other.x):
            if self.y1 > other.y:
                return True
            if screen_height - self.y2 < other.y + other.height:
                return True
        return False
