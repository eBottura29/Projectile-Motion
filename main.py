from pg_extensions import *


def start():
    pass


def update():
    global window
    window = get_window()

    set_window(window)


if __name__ == "__main__":
    run(start, update, 800, 450, False, "Ball Launcher Simulation", 60)
