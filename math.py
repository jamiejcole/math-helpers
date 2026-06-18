#!/usr/bin/env python3

from math import gcd
import sys

import readchar
from pyfiglet import Figlet

from rich.console import Console
from rich.panel import Panel
from rich.table import Table, box

console = Console()

MENU_ITEMS = [
    "Extended Euclidean Algorithm",
    "Bezout Coefficient table",
    "Rings and Fields Tables",
    "Exit",
]

def exit_gracefully():
    console.print("\nExiting...")
    raise SystemExit(0)

def clear():
    console.clear()


def title():
    fig = Figlet(font="small")
    ascii_title = fig.renderText("MATH SCRIPTS")

    console.print(f"[bold cyan]{ascii_title}[/bold cyan]")
    console.print(
        "[italic]A collection of 'I can't be fucked to do this' utilities for math[/italic]\n",
        style="yellow",
    )


def menu():
    selected = 0

    while True:
        clear()
        title()

        console.print(
            Panel.fit(
                "[bold green]Main Menu[/bold green]",
                border_style="green",
            )
        )

        console.print()

        for i, item in enumerate(MENU_ITEMS):
            number = i + 1

            if i == selected:
                console.print(
                    f"[black on bright_white]➜ {number}) {item}[/black on bright_white]"
                )
            else:
                console.print(f"  {number}) {item}")

        key = readchar.readkey()

        if key == readchar.key.UP:
            selected = (selected - 1) % len(MENU_ITEMS)

        elif key == readchar.key.DOWN:
            selected = (selected + 1) % len(MENU_ITEMS)

        elif key == readchar.key.ENTER:
            return selected

        elif key.isdigit():
            idx = int(key) - 1
            if 0 <= idx < len(MENU_ITEMS):
                return idx

        elif key == readchar.key.CTRL_C:
            exit_gracefully()

def extended_euclidean(a, b):
    rows = []

    r_prev, r = a, b
    s_prev, s = 1, 0
    t_prev, t = 0, 1

    while r != 0:
        q = r_prev // r

        rows.append([q, r_prev, r, s_prev, s, t_prev, t])

        r_prev, r = r, r_prev - q * r
        s_prev, s = s, s_prev - q * s
        t_prev, t = t, t_prev - q * t

    return rows, r_prev, s_prev, t_prev


def eea_menu():
    try:
        clear()
        title()

        console.print("[bold]Enter space-separated integers for the EEA.[/bold]")
        console.print("Example: 252 198\n")

        values = input("> ").strip().split()

        if len(values) != 2:
            console.print("\n[red]Currently expects exactly two numbers.[/red]")
            input("\nPress Enter...")
            return

        a, b = map(int, values)

        rows, gcd_value, x, y = extended_euclidean(a, b)

        table = Table(
            title=f"Extended Euclidean Algorithm ({a}, {b})",
            show_header=True,
            box=box.SQUARE,
        )

        table.add_column("q", justify="right")
        table.add_column("rₙ₋₁", justify="right")
        table.add_column("rₙ", justify="right")
        table.add_column("sₙ₋₁", justify="right")
        table.add_column("sₙ", justify="right")
        table.add_column("tₙ₋₁", justify="right")
        table.add_column("tₙ", justify="right")

        for row in rows:
            table.add_row(*map(str, row))

        console.print()
        console.print(table)

        console.print()
        console.print(f"[bold green]gcd({a}, {b}) = {gcd_value}[/bold green]")
        console.print(f"[bold cyan]{x}·{a} + {y}·{b} = {gcd_value}[/bold cyan]")

        input("\nPress Enter...")

    except KeyboardInterrupt:
        exit_gracefully()


def bezout_table():
    try:
        clear()
        title()

        console.print("[bold]Enter space-separated q values:[/bold]")
        console.print("Example: 1 2 3\n")

        q = list(map(int, input("> ").split()))

        x = [1, 0]
        y = [0, 1]

        for qi in q:
            x.append(x[-2] - qi * x[-1])
            y.append(y[-2] - qi * y[-1])

        table = Table(
            title="Extended Euclidean Algorithm",
            show_header=False,
            box=box.SQUARE,
        )

        total_cols = len(q) + 2

        for _ in range(total_cols):
            table.add_column(justify="center")

        table.add_row("qᵢ", "", "", *map(str, q))
        table.add_row("xᵢ", *map(str, x))
        table.add_row("yᵢ", *map(str, y))

        console.print()
        console.print(table)

        input("\nPress Enter...")

    except KeyboardInterrupt:
        exit_gracefully()


def rings_fields_menu():
    try:
        clear()
        title()

        console.print(
            "[bold]Enter n for ℤ*n and table size, space separated:[/bold]"
        )
        console.print("Example: 5 8\n")

        n, size = map(int, input("> ").split())

        console.print(
            "[bold]Multiplicative or Additive?[/bold] ([green]M[/green]/[cyan]A[/cyan])"
        )

        mode = input("> ").strip().lower()
        multiplicative = mode.startswith("m")

        title_text = (
            f"Multiplication Table Mod {n}"
            if multiplicative
            else f"Addition Table Mod {n}"
        )

        table = Table(title=title_text)

        table.add_column("")

        for col in range(size + 1):
            table.add_column(str(col), justify="center")

        for row in range(size + 1):
            values = []
            for col in range(size + 1):
                if multiplicative:
                    values.append(str((row * col) % n))
                else:
                    values.append(str((row + col) % n))

            table.add_row(str(row), *values)

        clear()
        title()
        console.print(table)

        input("\nPress Enter...")

    except KeyboardInterrupt:
        exit_gracefully()

def main():
    try:
        while True:
            choice = menu()

            if choice == 0:
                eea_menu()

            elif choice == 1:
                bezout_table()

            elif choice == 2:
                rings_fields_menu()

            elif choice == 3:
                break

    except KeyboardInterrupt:
        exit_gracefully()


if __name__ == "__main__":
    main()