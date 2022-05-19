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
        self.left_padel = Padel(0, height // 2, 20, height // 4, 6, 0)
        self.right_padel = Padel(width - 20, height // 2, 20, height // 4, 6, 1)
        self.duration = 0

        self.left_goals = 0
        self.right_goals = 0

        self.font = pygame.font.SysFont("Arial", 200, False, True)

    def run_frame(self, no_exit=False, wall=False):
        self.duration += 0.01
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        self.window.fill((0, 0, 0))

        text = self.font.render(
            f"{self.left_goals} : {self.right_goals}", True, (255, 0, 0)
        )
        self.window.blit(text, (200, 100))

        side = self.ball.move(self.width, self.height)
        if side == "left":
            self.right_score += 5
            self.right_goals += 1
            return True
        elif side == "right":
            if not wall:
                self.left_score += 5
                self.left_goals += 1
                return True

        coll = self.ball.collision(
            [self.left_padel, self.right_padel], wall, self.width
        )
        if coll == 0 and self.ball.lefthit:
            self.left_score += 1
            self.ball.lefthit = False
            self.ball.x_vel *= 1.1
            self.ball.y_vel *= 1.1
        elif coll == 1 and not self.ball.lefthit:
            self.right_score += 1
            self.ball.lefthit = True
            self.ball.x_vel *= 1.1
            self.ball.y_vel *= 1.1

        self.left_padel.draw(self.window)
        if not wall:
            self.right_padel.draw(self.window)

        self.ball.draw(self.window)
        pygame.display.update()
        if (self.left_score > 10 or self.duration > 30) and not no_exit:
            return True
        return False
