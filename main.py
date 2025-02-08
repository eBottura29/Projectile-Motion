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
    global position, v_i, theta, h_i, g, r, v_ix, v_iy, t, d_x, d_y, h_max, t_max, velocity, clicked, scale, positions
    window = get_window()

    velocity = Vector2()
    clicked = False

    v_i = 28  # m/s
    theta = 30  # deg
    h_i = 100  # m
    g = 9.8  # m/s2
    r = 25  # pixels
    scale = 10  # no units

    position = Vector2(-window.WIDTH // 2 + r, 0 if h_i > 0 else -window.HEIGHT // 2 + r)
    positions = []

    v_ix, v_iy, t, d_x, d_y, h_max, t_max = calculate(v_i, theta, h_i, g)


def update():
    global window, position, velocity, clicked
    window = get_window()
    window.SURFACE.fill(WHITE.tup())

    if input_manager.get_key_down(pygame.K_SPACE):
        velocity = Vector2(10, 10)
        clicked = True

    if clicked:
        velocity.y -= g * window.delta_time
        position += velocity * scale * window.delta_time
        positions.append(position)

    if position.y <= r - window.HEIGHT // 2:
        position.y = r - window.HEIGHT // 2
        velocity = Vector2()
        clicked = False

    for i, point in enumerate(positions):
        if i == 0:
            continue

        draw_line(window.SURFACE, BLACK, positions[i - 1], point, 2)

    draw_circle(window.SURFACE, GREEN, position, r)
    if h_i > 0:
        draw_rectangle(window.SURFACE, BLACK, Vector2(-window.WIDTH // 2, -r), Vector2(2 * r, window.HEIGHT), 2)

    values = Text(
        f"Initial Velocity: {v_i}\nAngle: {theta}\nInitial Height: {h_i}\nGravitational Force: {g}\n\nTime in Air: {t}\nDistance: {d_x}\nMaximum Height Above Initial Height: {h_max}\nTime to Reach Maximum Height: {t_max}",
        Text.arial_32,
        Vector2(4 * window.WIDTH // 5, 4 * window.HEIGHT // 5),
        Text.top_right,
        BLACK,
    )
    values.render()

    set_window(window)


if __name__ == "__main__":
    run(start, update, 800, 450, False, "Ball Launcher Simulation", 60)
