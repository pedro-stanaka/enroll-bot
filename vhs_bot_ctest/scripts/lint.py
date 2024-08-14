import subprocess


def format_and_lint():
    subprocess.run(["isort", "."], check=True)
    subprocess.run(["black", "."], check=True)
    subprocess.run(["pylint", "vhs_bot_ctest"], check=True)


if __name__ == "__main__":
    format_and_lint()
