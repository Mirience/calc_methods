from math import isfinite
from shutil import get_terminal_size


def right_side(x, v, t):
    return 4 * v * x**4 - 3 * v * t * x**3 + 6 * v * x - 2 * v * t


def exact_solution(x, v, t):
    return v * x**2 * (x - t)


def finite_difference(v, n):
    t = v
    h = t / n
    nodes = [k * h for k in range(n)] + [t]

    alpha = [0.0] * n
    beta = [0.0] * n
    y = [0.0] * (n + 1)

    # Прямой ход прогонки. y[k] = alpha[k] * y[k + 1] + beta[k].
    for k in range(1, n):
        x = nodes[k]

        a = 1 - h * x**2 / 2
        b = -2 + h**2 * x
        c = 1 + h * x**2 / 2
        d = h**2 * right_side(x, v, t)

        denominator = b + a * alpha[k - 1]
        if denominator == 0:
            raise ArithmeticError(f"Нулевой знаменатель прогонки в узле x{k}.")

        alpha[k] = -c / denominator
        beta[k] = (d - a * beta[k - 1]) / denominator

    # Обратный ход начинается с правого граничного значения y[n] = 0.
    for k in range(n - 1, 0, -1):
        y[k] = alpha[k] * y[k + 1] + beta[k]

    return nodes, y


def print_table(nodes, numerical, exact):
    errors = [y_num - y_exact for y_num, y_exact in zip(numerical, exact)]
    rows = [
        ("x_k", nodes),
        ("y_мет(x_k)", numerical),
        ("y_точн(x_k)", exact),
        ("e_k", errors),
    ]

    label_width = 13
    cell_width = 12
    terminal_width = get_terminal_size(fallback=(90, 24)).columns
    fitting_columns = (terminal_width - label_width - 1) // cell_width
    block_size = max(1, min(6, fitting_columns))

    for start in range(0, len(nodes), block_size):
        stop = min(start + block_size, len(nodes))
        columns = "".join(f"{f'x{k}':>{cell_width}}" for k in range(start, stop))

        print(f"{'Узел':<{label_width}}│{columns}")
        print("─" * label_width + "┼" + "─" * len(columns))

        for label, values in rows:
            cells = "".join(
                f"{value:>{cell_width}.4f}" for value in values[start:stop]
            )
            print(f"{label:<{label_width}}│{cells}")

        print()

    max_k = max(range(len(errors)), key=lambda k: abs(errors[k]))
    print(f"Максимальная |e_k| = {abs(errors[max_k]):.4f} в узле x{max_k}")


def main():
    try:
        v = float(input("Введите V [12]: ").strip().replace(",", ".") or "12")
        n = int(input("Введите число отрезков n [36]: ").strip() or "36")

        if not isfinite(v) or v <= 0:
            raise ValueError("V должно быть конечным положительным числом.")
        if n < 2:
            raise ValueError("Число отрезков n должно быть не меньше 2.")

        t = v
        nodes, numerical = finite_difference(v, n)
        exact = [0.0] + [exact_solution(x, v, t) for x in nodes[1:-1]] + [0.0]

    except (ValueError, ArithmeticError) as error:
        print(f"Ошибка: {error}")
        return

    print(f"\nV = T = {v:g}   n = {n}   h = {t / n:.6f}\n")
    print_table(nodes, numerical, exact)


if __name__ == "__main__":
    main()