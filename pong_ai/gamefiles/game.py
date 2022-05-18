import pygame, random
from .ball import Ball
from .padel import Padel


class Game:
    def __init__(self, window, width, height):
        self.window = window
        self.width, self.height = width, height
        self.ball = Ball(20, width // 2, height // 2)
        self.left_score = 0
        self.right_score = 0
        self.left_padel = Padel(0, height // 2, 20, height // 4, 12, 0)
        self.right_padel = Padel(width - 20, height // 2, 20, height // 4, 12, 1)

    def run_frame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        self.window.fill((0, 0, 0))

        side = self.ball.move(self.width, self.height)
        if side == "left":
            return True
        elif side == "right":
            return True

        coll = self.ball.collision([self.left_padel, self.right_padel])
        if coll == 0:
            self.left_score += 1
        elif coll == 1:
            self.right_score += 1

        self.left_padel.draw(self.window)
        self.right_padel.draw(self.window)

        self.ball.draw(self.window)
        pygame.display.update()
        if self.left_score + self.right_score > 20:
            return True
        return False
