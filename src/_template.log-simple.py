import logging
from pathlib import Path


def main() -> None:
    ...


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")

    logging.info("Command started...")
    main()
    logging.info("Finished command")
