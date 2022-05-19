import pygame, random


class Ball:
    def __init__(self, size, x, y):
        self.size = size
        self.direction = random.choice([-1, 1])
        self.lefthit = not self.direction
        self.y_direction = random.choice([-1, 1])
        self.x_vel = 7
        self.y_vel = 3
        self.x, self.y = x, y
        self.initial_x, self.initial_y = x, y

    def move(self, screen_width, screen_height):

        if self.x + self.x_vel * self.direction > screen_width:
            return "right"
        elif self.x + self.x_vel * self.direction < 0:
            return "left"
        elif self.y + self.y_vel * self.y_direction > screen_height:
            self.y_direction *= -1
        elif self.y + self.y_vel * self.y_direction < 0:
            self.y_direction *= -1

        self.x += self.x_vel * self.direction
        self.y += self.y_vel * self.y_direction
        return False

    def collision(self, paddles, wall, screen_width):
        for padel in paddles:
            if (self.x + self.size >= padel.x and self.x <= padel.x) or (
                wall and self.x + self.size >= screen_width - padel.width
            ):
                if (
                    self.y >= padel.y and self.y + self.size <= padel.y + padel.height
                ) or wall:
                    self.direction = abs(self.direction) * -1
                    return padel.index
            elif (
                self.x - self.size <= padel.x + padel.width
                and self.x >= padel.x + padel.width
            ):
                if self.y >= padel.y and self.y + self.size <= padel.y + padel.height:
                    self.direction = abs(self.direction)
                    return padel.index
        return 3

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 255), (self.x, self.y), self.size)

    def reset(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.direction = random.choice([-1, 1])
        self.y_direction = random.choice([-1, 1])
        self.y_vel = random.randint(1, 3)
        self.x_vel = 10 - self.y_vel
