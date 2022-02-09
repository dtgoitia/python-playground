#!/usr/bin/env python3

import shutil
import subprocess
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
PYTHON_VERSION = "3.10.0"
PYENV_DIR = Path("~/.pyenv").expanduser()

pyenv_python_path = PYENV_DIR / "versions" / PYTHON_VERSION / "bin/python"


class InstallationError(Exception):
    ...


def pyenv_is_in_path() -> bool:
    process = subprocess.run(["which", "pyenv"], capture_output=True)
    output = process.stdout.decode("utf-8")

    if not output:
        return False

    return True


def pyenv_has_python_version(version: str) -> bool:
    print(f"Checking that pyenv has Python {PYTHON_VERSION} installed...")
    process = subprocess.run(["pyenv", "versions", "--bare"], capture_output=True)
    output = process.stdout.decode("utf-8").strip()

    versions = {line for line in output.split("\n")}
    is_available = version in versions
    return is_available


def create_venv(venv_dir: Path) -> None:
    if not pyenv_is_in_path():
        raise InstallationError("Couldn't find `pyenv` in PATH")

    if not pyenv_has_python_version(PYTHON_VERSION):
        error_message = (
            f"pyenv does not have Python version {PYTHON_VERSION},"
            f" run: pyenv install {PYTHON_VERSION}"
        )
        raise InstallationError(error_message)

    print(f"Creating a Python {PYTHON_VERSION} venv with pyenv at {venv_dir}...")
    subprocess.run([pyenv_python_path, "-m", "venv", venv_dir], capture_output=False)


def delete_existing_venv(venv_dir: Path) -> None:
    print(f"Deleting {venv_dir} ...", end="")
    shutil.rmtree(venv_dir)
    assert venv_dir.exists() is False
    print(" done!")


def create_venv_if_does_not_exist(path: Path) -> Path:
    venv_dir = path / ".venv"
    if venv_dir.exists():
        print(f"A virtual environment already exists at {venv_dir}")

        response = ""
        YES = "y"
        NO = "n"
        while response not in {YES, NO}:
            response = input("Do you want to overwrite it? [y/n] ")
            response = response.lower()

        if response == NO:
            print("Nothing else will be done, bye!")
            exit()

        delete_existing_venv(venv_dir=venv_dir)

    create_venv(venv_dir=venv_dir)

    return venv_dir


def upgrade_pip(pip_path: Path) -> None:
    print(f"Upgrading pip to latest availble version...")
    subprocess.run([pip_path, "install", "--upgrade", "pip"])


def install_dev_dependencies(pip_path: Path) -> None:
    dev_requirements_path = REPO_DIR / "requirements" / "dev.txt"
    print(f"Installing development dependencies from {dev_requirements_path} ...")
    subprocess.run([pip_path, "install", "-r", dev_requirements_path])


def set_up_development_environment() -> None:
    venv_dir = create_venv_if_does_not_exist(path=REPO_DIR)
    venv_pip_path = venv_dir / "bin/pip"
    upgrade_pip(pip_path=venv_pip_path)
    install_dev_dependencies(pip_path=venv_pip_path)


if __name__ == "__main__":
    set_up_development_environment()
