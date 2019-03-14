#!/usr/bin/env python3

import time
import os
import random
import sys


class Singleton(object):
  _instances = {}

  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
        class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
    return class_._instances[class_]


class Grid:
    def __init__(self, rows: int, cols: int):
        self.grid = self.create_initial_grid(rows, cols)
        self.live_neighbors = self.get_live_neighbors(rows, cols, self.grid)

    def create_initial_grid(self, rows: int, cols: int):
        """
        Creates a random list of lists that contains 1s and 0s to represent the cells in Conway's Game of Life.
        #TODO Создает случайный список списков, который содержит 1 и 0 для представления ячеек в игре жизни Конвея.
        :param rows: Int - The number of rows that the Game of Life grid will have
        :param cols: Int - The number of columns that the Game of Life grid will have
        :return: Int[][] - A list of lists containing 1s for live cells and 0s for dead cells
        """
        grid = []
        for row in range(rows):
            grid_rows = []
            for col in range(cols):
                # Generate a random number and based on that decide whether to add a live or dead cell to the grid
                if random.randint(0, 7) == 0:
                    grid_rows += [1]
                else:
                    grid_rows += [0]
            grid += [grid_rows]
        return grid


    def get_live_neighbors(self, rows: int, cols: int, grid: list):
        """
        Counts the number of live cells surrounding a center cell at grid[row][cell].
        #TODO: Подсчитывает количество живых клеток, окружающих центральную ячейку в сетке [строка] [ячейка].
        :param row: Int - The row of the center cell
        :param col: Int - The column of the center cell
        :param rows: Int - The number of rows that the Game of Life grid has
        :param cols: Int - The number of columns that the Game of Life grid has
        :param grid: Int[][] - The list of lists that will be used to represent the Game of Life grid
        :return: Int - The number of live cells surrounding the cell at grid[row][cell]
        """
        def __get_live_sun(row: int, col: int, rows: int, cols: int, grid: list):
            life_sum = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # Make sure to count the center cell located at grid[row][col]
                    if not (i == 0 and j == 0):
                        # Using the modulo operator (%) the grid wraps around
                        life_sum += grid[((row + i) % rows)][((col + j) % cols)]
            return life_sum

        live_neighbors = []
        for row in range(rows):
            elements = []
            for col in range(cols):
                # Get the number of live cells adjacent to the cell at grid[row][col]
                elements.append(__get_live_sun(row, col, rows, cols, grid))
            live_neighbors.append(elements)
        return live_neighbors


class Game(Singleton):
    def __init__(self):
        self.name = 'Game of Life'

    @staticmethod
    def clear_console():
        """
        Clears the console using a system command based on the user's operating system.

        """

        if sys.platform.startswith('win'):
            os.system("cls")
        elif sys.platform.startswith('linux'):
            os.system("clear")
        else:
            print("Unable to clear terminal. Your operating system is not supported.\n\r")

    @staticmethod
    def resize_console(rows: int, cols: int):
        """
        Re-sizes the console to the size of rows x columns

        :param rows: Int - The number of rows for the console to re-size to
        :param cols: Int - The number of columns for the console to re-size to
        """

        if cols < 32:
            cols = 32

        if sys.platform.startswith('win'):
            command = "mode con: cols={0} lines={1}".format(cols + cols,
                                                            rows + 5)
            os.system(command)
        elif sys.platform.startswith('linux'):
            command = "\x1b[8;{rows};{cols}t".format(rows=rows + 3,
                                                     cols=cols + cols)
            sys.stdout.write(command)
        else:
            print(
                "Unable to resize terminal. Your operating system is not supported.\n\r")


    def print_grid(self, rows: int, cols: int, grid: Grid, generation: int):
        """
        Prints to console the Game of Life grid
        #TODO: prints сетки Game of Life
        :param rows: Int - The number of rows that the Game of Life grid has
        :param cols: Int - The number of columns that the Game of Life grid has
        :param grid: Int[][] - The list of lists that will be used to represent the Game of Life grid
        :param generation: Int - The current generation of the Game of Life grid
        """

        self.clear_console()

        # A single output string is used to help reduce the flickering caused by printing multiple lines
        output_str = ""

        # Compile the output string together and then print it to console
        output_str += "Generation {0} - To exit the program early press <Ctrl-C>\n\r".format(
            generation)
        for row in range(rows):
            for col in range(cols):
                if grid.grid[row][col] == 0:
                    output_str += ". "
                else:
                    output_str += "@ "
            output_str += "\n\r"
        print(output_str, end=" ")

    def create_next_grid(self, rows: int, cols: int, grid: Grid, next_grid: Grid):
        """
        Analyzes the current generation of the Game of Life grid and determines what cells live and die in the next
        generation of the Game of Life grid.
        #TODO: Анализирует текущее поколение сетки Игры Жизни и определяет, какие клетки живут и умирают в следующем поколение сетки Игры Жизни.
        :param rows: Int - The number of rows that the Game of Life grid has
        :param cols: Int - The number of columns that the Game of Life grid has
        :param grid: Int[][] - The list of lists that will be used to represent the current generation Game of Life grid
        :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Game of Life
        grid
        """

        for row in range(rows):
            for col in range(cols):
                # Get the number of live cells adjacent to the cell at grid[row][col]
                live_neighbors = grid.live_neighbors[row][col]

                # If the number of surrounding live cells is < 2 or > 3 then we make the cell at grid[row][col] a dead cell
                if live_neighbors < 2 or live_neighbors > 3:
                    next_grid.grid[row][col] = 0
                # If the number of surrounding live cells is 3 and the cell at grid[row][col] was previously dead then make
                # the cell into a live cell
                elif live_neighbors == 3 and grid.grid[row][col] == 0:
                    next_grid.grid[row][col] = 1
                # If the number of surrounding live cells is 3 and the cell at grid[row][col] is alive keep it alive
                else:
                    next_grid.grid[row][col] = grid.grid[row][col]

    def grid_changing(self, grid: Grid, next_grid: Grid):
        """
        Checks to see if the current generation Game of Life grid is the same as the next generation Game of Life grid.
        #TODO: Проверяет, совпадает ли сетка Game of Life текущего поколения с сеткой Game of Life следующего поколения.
        :param rows: Int - The number of rows that the Game of Life grid has
        :param cols: Int - The number of columns that the Game of Life grid has
        :param grid: Int[][] - The list of lists that will be used to represent the current generation Game of Life grid
        :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Game of Life
        grid
        :return: Boolean - Whether the current generation grid is the same as the next generation grid
        """
        return grid != next_grid

    def get_integer_value(self, prompt: str, low: int, high: int):
        """
        Asks the user for integer input and between given bounds low and high.
        #TODO: Запрашивает у пользователя целочисленный ввод и между заданными границами - низким и высоким.
        :param prompt: String - The string to prompt the user for input with
        :param low: Int - The low bound that the user must stay within
        :param high: Int - The high bound that the user must stay within
        :return: The valid input value that the user entered
        """

        while True:
            try:
                value = int(input(prompt))
            except ValueError:
                print("Input was not a valid integer value.")
                continue
            if value < low or value > high:
                print(
                    "Input was not inside the bounds (value <= {0} or value >= {1}).".format(
                        low, high))
            else:
                break
        return value

    def run_game(self):
        """
        #TODO: Запрашивает у пользователя вводные данные, чтобы настроить игру «Жизнь» на определенное количество поколений.
        Asks the user for input to setup the Game of Life to run for a given number of generations.

        """

        self.clear_console()

        # Get the number of rows and columns for the Game of Life grid
        rows = self.get_integer_value("Enter the number of rows (10-60): ", 10, 60)
        cols = self.get_integer_value("Enter the number of cols (10-118): ", 10, 118)

        # Get the number of generations that the Game of Life should run for
        generations = self.get_integer_value(
            "Enter the number of generations (1-100000): ", 1, 100000)
        self.resize_console(rows, cols)

        # Create the initial random Game of Life grids
        current_generation = Grid(rows, cols)
        next_generation = Grid(rows, cols)

        # Run Game of Life sequence
        gen = 1
        for gen in range(1, generations + 1):
            if not self.grid_changing(current_generation, next_generation):
                break
            self.print_grid(rows, cols, current_generation, gen)
            self.create_next_grid(rows, cols, current_generation, next_generation)
            time.sleep(1 / 5.0)
            current_generation, next_generation = next_generation, current_generation

        self.print_grid(rows, cols, current_generation, gen)
        input("Press <Enter> to exit.")


game = Game()
game.run_game()

