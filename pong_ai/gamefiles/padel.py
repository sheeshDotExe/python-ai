import pygame


class Padel:
    def __init__(self, x, y, width, height, speed, index):
        self.x, self.y = x, y - height // 2
        self.width, self.height = width, height
        self.speed = speed
        self.index = index

    def move(self, direction, screen_height):
        if self.y + self.height + self.speed * direction > screen_height:
            return False
        elif self.y + self.speed * direction < 0:
            return False
        self.y += self.speed * direction
        return True

    def draw(self, window):
        pygame.draw.rect(
            window, (255, 255, 0), (self.x, self.y, self.width, self.height)
        )
