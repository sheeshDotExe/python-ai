from ai import Training_model
import os


def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    training = Training_model(config_path)

    training.run_neat(os.path.join(local_dir, "checkpoints"), 60)
    # training.play_against_best_ai()


if __name__ == "__main__":
    main()
