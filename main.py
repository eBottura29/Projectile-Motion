from pg_extensions import *


def calculate(v_i, theta, h_i, g, debug=False):
    v_ix = v_i * math.cos(math.radians(theta))
    v_iy = v_i * math.sin(math.radians(theta))

    d_y = -h_i
    a = -g

    t1 = (-v_iy + (v_iy**2 + 2 * a * d_y) ** 0.5) / a
    t2 = (-v_iy - (v_iy**2 + 2 * a * d_y) ** 0.5) / a

    t = t1 if t1 > t2 else t2

    if debug:
        print(t)

    d_x = v_ix * t

    if debug:
        print(d_x)

    h_max = ((v_iy) ** 2) / (2 * g)

    if debug:
        print(h_max)

    t_max = v_iy / g

    if debug:
        print(t_max)

    return v_ix, v_iy, t, d_x, d_y, h_max, t_max


def start():
    global position, v_i, theta, h_i, g, r, v_ix, v_iy, t, d_x, d_y, h_max, t_max
    window = get_window()

    v_i = 8.5  # m/s
    theta = 30  # deg
    h_i = 100  # m
    g = 9.8  # m/s2
    r = 25

    position = Vector2(-window.WIDTH // 2 + r, -window.HEIGHT // 2 + r if h_i == 0 else 0)

    v_ix, v_iy, t, d_x, d_y, h_max, t_max = calculate(v_i, theta, h_i, g)


def update():
    global window
    window = get_window()
    window.SURFACE.fill(WHITE.tup())

    draw_circle(window.SURFACE, BLACK, position, r)

    set_window(window)


if __name__ == "__main__":
    run(start, update, 800, 450, False, "Ball Launcher Simulation", 60)
