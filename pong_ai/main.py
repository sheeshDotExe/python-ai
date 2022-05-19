from ai import Training_model
import os
import pygame


def main():
    pygame.font.init()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    training = Training_model(config_path)

    train = False

    if train:
        training.run_neat(
            os.path.join(local_dir, "checkpoints"),
            10,
            wall=True,
            load_prev=False,
            CHECKPOINT=9,
        )
    else:
        training.play_against_best_ai()


if __name__ == "__main__":
    main()
