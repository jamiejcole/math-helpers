#!/usr/bin/env python3

from math import gcd
import sys
import argparse

import readchar
from pyfiglet import Figlet

from rich.console import Console
from rich.panel import Panel
from rich.table import Table, box
from math import gcd

console = Console()

MENU_ITEMS = [
    "Extended Euclidean Algorithm",
    "Bezout Coefficient table",
    "Rings and Fields Tables",
    "Z* Sets",
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

def build_eea_columns(a, b):
    r = [a, b]
    x = [1, 0]
    y = [0, 1]
    q = ["", ""]  # placeholders for r0, r1 columns

    while True:
        if r[-1] == 0:
            break

        qi = r[-2] // r[-1]
        q.append(qi)

        r.append(r[-2] - qi * r[-1])
        x.append(x[-2] - qi * x[-1])
        y.append(y[-2] - qi * y[-1])

        if r[-1] == 0:
            break

    return q, r, x, y

def z_sets_menu():
    try:
        clear()
        title()

        console.print("[bold]Enter two values n1 n2:[/bold]")
        console.print("Example: 16 20\n")

        n1, n2 = map(int, input("> ").split())

        from math import gcd

        left = Table(title=f"ℤ*{n1} (gcd)")
        left.add_column("x", justify="right")
        left.add_column(f"gcd(x,{n1})", justify="right")

        right = Table(title=f"ℤ*{n2} (gcd)")
        right.add_column("x", justify="right")
        right.add_column(f"gcd(x,{n2})", justify="right")

        rows = max(n1 - 1, n2 - 1)

        coprime_both = []

        for i in range(1, rows + 1):

            # left table
            if i < n1:
                g1 = gcd(i, n1)
                left.add_row(str(i), str(g1))
            else:
                left.add_row("", "")

            # right table
            if i < n2:
                g2 = gcd(i, n2)
                right.add_row(str(i), str(g2))
            else:
                right.add_row("", "")

            # intersection condition
            if i < n1 and i < n2:
                if gcd(i, n1) == 1 and gcd(i, n2) == 1:
                    coprime_both.append(i)

        clear()
        title()

        from rich.columns import Columns
        console.print(Columns([left, right], equal=True))

        console.print("\n[bold cyan]Common coprime elements:[/bold cyan]")
        console.print(coprime_both)

        input("\nPress Enter...")

    except KeyboardInterrupt:
        exit_gracefully()
        
def display_eea_table(a, b):
    """Helper function to calculate and render the EEA table cleanly."""
    q, r, x, y = build_eea_columns(a, b)
    cols = len(q)

    table = Table(
        title=f"Extended Euclidean Algorithm ({a}, {b})",
        show_header=False,
        box=box.SQUARE,
        pad_edge=False,
    )

    for _ in range(cols):
        table.add_column(justify="center")

    table.add_row("qᵢ", *map(str, q))
    table.add_row("rᵢ", *map(str, r))
    table.add_row("xᵢ", *map(str, x))
    table.add_row("yᵢ", *map(str, y))

    console.print()
    console.print(table)

    # final Bézout identity
    g = r[-2] if r[-1] == 0 else r[-1]
    console.print(f"\n[bold green]gcd = {g}[/bold green]")
    console.print(f"[cyan]{x[-2]}·{a} + {y[-2]}·{b} = {g}[/cyan]")


def eea_menu():
    try:
        clear()
        title()

        console.print("[bold]Enter two integers:[/bold]")
        console.print("Example: 377 3434\n")

        a, b = map(int, input("> ").split())
        display_eea_table(a, b)

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

            row_vals = []
            has_one = False

            for col in range(size + 1):
                val = (row * col) % n if multiplicative else (row + col) % n
                row_vals.append(val)

                if multiplicative and val == 1 and row != 0 and col != 0:
                    has_one = True

            if multiplicative and row != 0 and has_one:
                first_col = f"[green]{row}[/green]"
            else:
                first_col = str(row)

            for col, val in enumerate(row_vals):
                if multiplicative:
                    if val == 1 and row != 0 and col != 0:
                        values.append("[green]1[/green]")
                    else:
                        values.append(str(val))
                else:
                    values.append(str(val))

            table.add_row(first_col, *values)

        clear()
        title()
        console.print(table)

        input("\nPress Enter...")

    except KeyboardInterrupt:
        exit_gracefully()

def main():
    # Setup CLI argument options
    parser = argparse.ArgumentParser(description="Math utilities shortcut.")
    parser.add_argument(
        "-e", 
        nargs=2, 
        type=int, 
        metavar=("NUM1", "NUM2"), 
        help="Directly run Extended Euclidean Algorithm with two numbers"
    )
    
    args = parser.parse_args()

    # If the shortcut flag is provided, execute it immediately and bypass menu loop
    if args.e:
        try:
            display_eea_table(args.e[0], args.e[1])
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
        return

    # Normal menu loop
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
                z_sets_menu()

            elif choice == 4:
                break

    except KeyboardInterrupt:
        exit_gracefully()


if __name__ == "__main__":
    main()