import logging
from pathlib import Path


def main() -> None:
    ...


if __name__ == "__main__":
    log_file = Path(f"{__file__}.log")
    log_format = "%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format=log_format)

    logging.info("Command started...")
    main()
    logging.info("Finished command")
