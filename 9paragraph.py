from decimal import Decimal, InvalidOperation, getcontext

getcontext().prec = 40

DEFAULT_STEPS = (Decimal("1"), Decimal("0.1"), Decimal("0.01"))
STEP_COUNT = 9


def f(x, y, v):
    return 2 * v * x + v * x**2 - y


def euler(x, y, h, v):
    return y + h * f(x, y, v)


def improved_euler(x, y, h, v):
    next_x = x + h
    return (y + h * v * (2 * next_x + next_x**2)) / (1 + h)


def predictor_corrector(x, y, h, v):
    left_slope = f(x, y, v)
    predicted = y + h * left_slope
    right_slope = f(x + h, predicted, v)
    return y + h * (left_slope + right_slope) / 2


def solve(method, h, v):
    nodes = [1 + k * h for k in range(STEP_COUNT + 1)]
    numerical = [v]

    for x in nodes[:-1]:
        numerical.append(method(x, numerical[-1], h, v))

    exact = [v * x**2 for x in nodes]
    errors = [approx - true for approx, true in zip(numerical, exact)]
    return nodes, numerical, exact, errors


def print_table(nodes, numerical, exact, errors):
    rows = [
        ["Узлы xₖ"] + [f"x{k}={x.normalize():f}" for k, x in enumerate(nodes)],
        ["Метод yₘ"] + [f"{y:.16g}" for y in numerical],
        ["Точное yₜ"] + [f"{y:.16g}" for y in exact],
        ["Ошибка eₖ"] + [f"{e:+.6e}" if e else "0" for e in errors],
    ]
    widths = [max(map(len, column)) for column in zip(*rows)]

    def border(left, middle, right):
        return left + middle.join("─" * (width + 2) for width in widths) + right

    print(border("┌", "┬", "┐"))

    for index, row in enumerate(rows):
        label, *values = row
        cells = [f" {label:<{widths[0]}} "]
        cells.extend(
            f" {value:>{width}} "
            for value, width in zip(values, widths[1:])
        )
        print("│" + "│".join(cells) + "│")

        if index == 0:
            print(border("├", "┼", "┤"))

    print(border("└", "┴", "┘"))


def read_variant():
    while True:
        value = input("Введите V (Enter для V = 1): ").strip()

        try:
            v = Decimal(value.replace(",", ".")) if value else Decimal("1")
            if v.is_finite():
                return v
        except InvalidOperation:
            pass

        print("Введите конечное число для V.")


def read_steps():
    while True:
        value = input(
            "Введите шаг h или несколько через пробел "
            "(Enter — 1 0.1 0.01): "
        ).strip()

        if not value:
            return DEFAULT_STEPS

        try:
            steps = [Decimal(part.replace(",", ".")) for part in value.split()]
        except InvalidOperation:
            print("Введите числа, например 0.00001 или 1 0.1 0.01.")
            continue

        if all(h.is_finite() and h > 0 for h in steps):
            return steps

        print("Каждый шаг должен быть конечным положительным числом.")


def main():
    v = read_variant()
    steps = read_steps()

    methods = (
        ("Метод Эйлера", euler),
        ("Усовершенствованный метод Эйлера", improved_euler),
        ("Метод прогноза и коррекции", predictor_corrector),
    )

    print(f"\nЗадача Коши · V = {v}")
    print("Погрешность eₖ = yₘ(xₖ) − yₜ(xₖ)")

    for h in steps:
        print(f"\n{'═' * 20}  Шаг h = {h}  {'═' * 20}")

        for name, method in methods:
            print(f"\n{name}")
            print_table(*solve(method, h, v))


if __name__ == "__main__":
    main()