from pg_extensions import *


def calculate(v_i, theta, h_i, g):
    v_ix = v_i * math.cos(math.radians(theta))
    v_iy = v_i * math.sin(math.radians(theta))

    d_y = -h_i
    a = -g

    t1 = (-v_iy + (v_iy**2 + 2 * a * d_y) ** 0.5) / a
    t2 = (-v_iy - (v_iy**2 + 2 * a * d_y) ** 0.5) / a

    t = t1 if t1 > t2 else t2

    print(t)

    d_x = v_ix * t

    print(d_x)

    h_max = ((v_iy) ** 2) / (2 * g)

    print(h_max)

    t_max = v_iy / g

    print(t_max)

    return v_ix, v_iy, t, d_x, d_y, h_max, t_max


def start():
    pass


def update():
    global window
    window = get_window()

    v_i = 8.5  # m/s
    theta = 30  # deg
    h_i = 100  # m
    g = -9.8  # m/s2

    v_ix, v_iy, t, d_x, d_y, h_max, t_max = calculate(v_i, theta, h_i, g)

    set_window(window)


if __name__ == "__main__":
    run(start, update, 800, 450, False, "Ball Launcher Simulation", 60)
