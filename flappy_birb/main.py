from fileinput import filename
import pygame, random, neat, pickle, os
from gamefiles import Bird, Pipe


class Game:
    def __init__(self, width, height, win):
        self.width, self.height = width, height
        self.clock = pygame.time.Clock()
        self.win = win
        self.gap = 300
        self.low, self.high = 70, 300

    def run(self, genomes, config, draw=True, fitness_update=True):

        birds = []

        for (_, genome) in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            birds.append(Bird(self.width, self.height, net))

        run = True
        pipes = []

        points = 0

        for i in range(3):
            y1 = random.randint(10, 400)
            y2 = self.height - (y1 + random.randint(self.low, self.high))
            pipes.append(Pipe(self.width + i * self.gap, y1, y2))

        while run:
            points += 0.1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.win.fill((0, 0, 0))

            low_x = 1000
            y_vals = [0, 0]

            for j, pipe in enumerate(pipes):
                if pipe.x + pipe.width > self.width / 2:
                    if pipe.x < low_x:
                        low_x = pipe.x
                        y_vals[0] = pipe.y1
                        y_vals[1] = pipe.y2

                if pipe.move():
                    x = 0
                    for k in pipes:
                        if k.x > x:
                            x = k.x

                    y1 = random.randint(10, 400)
                    y2 = self.height - (y1 + random.randint(self.low, self.high))
                    pipes[j] = Pipe(x + self.gap, y1, y2)
                if draw:
                    pipe.draw(self.win, self.height)

            eval = True
            for bird in birds:
                if bird.alive:
                    bird.score = points
                    eval = False
                    bird.move(y_vals)
                    if draw:
                        bird.draw(self.win)

                    for pipe in pipes:
                        if pipe.checkcollision(bird, self.height):
                            bird.alive = False

            if eval or points > 800:
                if fitness_update:
                    self.calculate_fitness(genomes, birds)
                break

            pygame.display.update()

    def calculate_fitness(self, genomes, birds):
        for (_, genome), bird in zip(genomes, birds):
            genome.fitness += bird.score


def eval_genomes(genomes, config):
    width, height = 700, 500
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("flapy birb?")

    game = Game(width, height, win)
    game.run(genomes, config)


def run_neat(config, checkpointpath):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(
        neat.Checkpointer(
            500, filename_prefix=os.path.join(checkpointpath, "neat-checkpoit-")
        )
    )

    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def main():

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    if input("new y/n? ") == "n":
        with open("best.pickle", "rb") as f:
            winner = pickle.load(f)
            while 1:
                eval_genomes([(0, winner)], config)
    else:
        # game = Game(width, height)
        run_neat(config, os.path.join(local_dir, "checkpoints"))


if __name__ == "__main__":
    main()
