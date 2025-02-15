from pg_extensions import *


def calculate(v_i, theta, h_i, g, debug=False):
    global v_ix, v_iy, t, d_x, d_y, h_max, t_max

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


def render_ui():
    global activated_before

    values1 = Text(
        f"Initial Velocity: {v_i:.2f} m/s",
        Text.arial_16,
        Vector2(2 * window.WIDTH // 5, 2 * window.HEIGHT // 5 - 0),
        Text.top_right,
        BLACK,
    )
    values1.render()

    values2 = Text(
        f"Angle: {theta:.2f}°",
        Text.arial_16,
        Vector2(2 * window.WIDTH // 5, 2 * window.HEIGHT // 5 - 32),
        Text.top_right,
        BLACK,
    )
    values2.render()

    values3 = Text(
        f"Initial Height: {h_i:.2f} m",
        Text.arial_16,
        Vector2(2 * window.WIDTH // 5, 2 * window.HEIGHT // 5 - 64),
        Text.top_right,
        BLACK,
    )
    values3.render()

    values4 = Text(
        f"Gravitational Force: {g:.2f} m/s^2",
        Text.arial_16,
        Vector2(2 * window.WIDTH // 5, 2 * window.HEIGHT // 5 - 96),
        Text.top_right,
        BLACK,
    )
    values4.render()

    values5 = Text(
        f"Time in Air: {t if activated_before else 0:.2f} s",
        Text.arial_16,
        Vector2(2 * window.WIDTH // 5, 2 * window.HEIGHT // 5 - 160),
        Text.top_right,
        BLACK,
    )
    values5.render()

    values6 = Text(
        f"Distance: {d_x if activated_before else 0:.2f} m",
        Text.arial_16,
        Vector2(2 * window.WIDTH // 5, 2 * window.HEIGHT // 5 - 192),
        Text.top_right,
        BLACK,
    )
    values6.render()

    values7 = Text(
        f"Maximum Height Above Initial Height: {h_max if activated_before else 0:.2f} m",
        Text.arial_16,
        Vector2(2 * window.WIDTH // 5, 2 * window.HEIGHT // 5 - 224),
        Text.top_right,
        BLACK,
    )
    values7.render()

    values8 = Text(
        f"Time to Reach Maximum Height: {t_max if activated_before else 0:.2f} s",
        Text.arial_16,
        Vector2(2 * window.WIDTH // 5, 2 * window.HEIGHT // 5 - 256),
        Text.top_right,
        BLACK,
    )
    values8.render()

    disclaimer = Text(
        f"*animation not to scale",
        Text.arial_16,
        Vector2(2 * window.WIDTH // 5, 2 * window.HEIGHT // 5 - 288),
        Text.top_right,
        BLACK,
    )
    disclaimer.render()

    if not activated_before:
        tutorial = Text(
            f"Press the Space Bar to Simulate",
            Text.arial_24,
            Vector2(-2 * window.WIDTH // 5, 2 * window.HEIGHT // 5),
            Text.top_left,
            BLACK,
        )
        tutorial.render()


def start():
    global position, v_i, theta, h_i, g, r, velocity, clicked, scale, positions, activated_before
    window = get_window()

    velocity = Vector2()
    clicked = False
    activated_before = False

    v_i = random_float(1, 100)  # m/s
    theta = random_float(0, 89.99)  # deg
    h_i = random_float(0, 100) * random.randint(0, 1)  # m
    g = 9.81  # m/s2
    r = 25  # pixels
    scale = 10  # no units

    position = Vector2(-window.WIDTH // 2 + r, 0 if h_i > 0 else -window.HEIGHT // 2 + r)
    positions = []


def update():
    global window, position, velocity, clicked, activated_before, v_ix, v_iy, t, d_x, d_y, h_max, t_max
    window = get_window()
    window.SURFACE.fill(WHITE.tup())

    if input_manager.get_key_down(pygame.K_SPACE) and not activated_before:
        velocity = Vector2(10, 10)
        clicked = True
        activated_before = True

        v_ix, v_iy, t, d_x, d_y, h_max, t_max = calculate(v_i, theta, h_i, g)

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

    render_ui()

    set_window(window)


if __name__ == "__main__":
    run(start, update, 800, 450, False, "Projectile Motion Simulation", 60)
