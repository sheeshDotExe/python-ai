import pygame, neat, os, pickle
from gamefiles import Game


class Training_model:
    def __init__(self, config_path):
        self.config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path,
        )

    def calculate_fitness(self, genome1, genome2, game):
        genome1.fitness += game.left_score + game.duration
        genome2.fitness += game.right_score + game.duration

    def calculate_fitness_2(self, genome, game):
        # print(game.left_score)
        genome.fitness += game.left_score + game.duration

    def eval_genomes_against_wall(self, genomes, config):
        clock = pygame.time.Clock()
        width, height = 800, 800
        window = pygame.display.set_mode((width, height))

        for _, genome in genomes:
            genome.fitness = 0
            game = Game(window, width, height)

            net = neat.nn.FeedForwardNetwork.create(genome, config)

            while True:
                output = net.activate(
                    (
                        game.left_padel.y + game.left_padel.width // 2,
                        abs(game.left_padel.x - game.ball.x),
                        game.ball.y,
                    )
                )
                decision = output.index(max(output))
                valid = True
                if decision == 0:
                    genome.fitness -= 0.0
                elif decision == 1:
                    if not game.left_padel.move(-1, game.height):
                        valid = False
                else:
                    if not game.left_padel.move(1, game.height):
                        valid = False

                if not valid:
                    genome.fitness -= 0.0

                if game.run_frame(wall=True):
                    self.calculate_fitness_2(genome, game)
                    break

    def eval_genomes(self, genomes, config):
        clock = pygame.time.Clock()
        width, height = 800, 800
        window = pygame.display.set_mode((width, height))

        for i, (_, genome1) in enumerate(genomes):
            genome1.fitness = 0
            for _, genome2 in genomes[min(i + 1, len(genomes) - 1) :]:
                genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
                game = Game(window, width, height)

                net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
                net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

                while True:
                    # clock.tick(60)
                    players = [
                        (genome1, net1, game.left_padel),
                        (genome2, net2, game.right_padel),
                    ]
                    for (genome, net, paddle) in players:
                        output = net.activate(
                            (
                                paddle.y + paddle.width // 2,
                                abs(paddle.x - game.ball.x),
                                game.ball.y,
                            )
                        )
                        decision = output.index(max(output))
                        valid = True
                        if decision == 0:
                            genome.fitness -= 0.1
                        elif decision == 1:
                            if not paddle.move(-1, game.height):
                                valid = False
                        else:
                            if not paddle.move(1, game.height):
                                valid = False

                        if not valid:
                            genome.fitness -= 0.5

                    if game.run_frame():
                        self.calculate_fitness(genome1, genome2, game)
                        break

    def run_neat(
        self, checkpointpath, generations=50, wall=False, load_prev=True, CHECKPOINT=0
    ):
        if load_prev:
            p = neat.Checkpointer.restore_checkpoint(
                os.path.join(checkpointpath, "neat-checkpoit-%i" % CHECKPOINT)
            )
        else:
            p = neat.Population(self.config)
            p.add_reporter(neat.StdOutReporter(True))
            stats = neat.StatisticsReporter()
            p.add_reporter(stats)
            p.add_reporter(
                neat.Checkpointer(
                    5, filename_prefix=os.path.join(checkpointpath, "neat-checkpoit-")
                )
            )

        if wall:
            winner = p.run(self.eval_genomes_against_wall, generations)
        else:
            winner = p.run(self.eval_genomes, generations)
        with open("best.pickle", "wb") as f:
            pickle.dump(winner, f)

    def play_against_best_ai(self):

        try:
            with open("best.pickle", "rb") as f:
                winner = pickle.load(f)
        except IOError:
            print("no trained ai")

        clock = pygame.time.Clock()
        width, height = 800, 800
        window = pygame.display.set_mode((width, height))
        game = Game(window, width, height)
        player_decision = 0
        net = neat.nn.FeedForwardNetwork.create(winner, self.config)

        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player_decision = -1
                    elif event.key == pygame.K_s:
                        player_decision = 1
                elif event.type == pygame.KEYUP:
                    player_decision = 0

            game.left_padel.move(player_decision, game.height)

            output = net.activate(
                (
                    game.right_padel.y + game.right_padel.width // 2,
                    abs(game.right_padel.x - game.ball.x),
                    game.ball.y,
                )
            )
            decision = output.index(max(output))
            if decision == 0:
                pass
            elif decision == 1:
                game.right_padel.move(-1, game.height)
            else:
                game.right_padel.move(1, game.height)

            if game.run_frame(True):
                game.ball.reset()
