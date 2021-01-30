from Bot import Bot
from copy import copy
from random import randint
from graf import math_expr

def get_random_coordinates(x, y):
    return randint(0, x - 1), randint(0, y - 1)


class Cell:
    def __init__(self, value=0, index=None):
        self.value = value  # значение ячейки: 0 - пусто, 1 - бот, 2 - еда, 3 - яд, 4 - стена
        if self.value == 1:
            self.index = index  # index -- номер бота в ячейки

    def __str__(self):
        return str(self.value)

    def change_value(self, value):
        self.value = value

    def change_index(self, index):
        self.index = index


class Arena:
    def __init__(self, root_window, length, height, count_of_bots, start_poison, start_food,
                 end_count, genes_mutation, number_mutation, walls):
        self.walls = walls
        self.window = root_window
        self.count_of_bots = count_of_bots
        self.end_count = end_count
        self.length = length  # по координате x
        self.height = height  # по координате y
        self.start_poison = start_poison #начальное количество яда
        self.start_food = start_food #начальное количество еды
        self.genes_mutation = genes_mutation
        self.number_mutation = number_mutation
        self.bot_number = 0 #счётчик ботов
        self.flag_finish = False #флаг конца хода бота
        self.flag_skip = False #нужно ли пропускать ходы?
        self.gen = 0
        self.count_move = 0
        self.kol_of_move = []
        # доска, на которой происходит всё действие
        self.board = [[Cell() for i in range(self.height)] for j in range(self.length)]
        # массив ботов
        self.bots = [Bot(self.window.ui) for i in range(self.count_of_bots)]
        self.make_walls()

    def __str__(self):
        a = ''
        for i in range(self.height - 1, -1, -1):
            for j in range(self.length):
                a += str(self.board[j][i])
                if j == self.length - 1:
                    a += '\n'
                else:
                    a += ' '
        return a

    def make_walls(self):
        for i in self.walls:
            self.board[i[0]][i[1]].change_value(4)
            self.window.ui.ColorConfiguration(4, i[0], i[1], 0)

    # закидывает на арену ботов
    def make_bots(self):
        i = 0
        while i < self.count_of_bots:
            # две рандомных координаты
            x, y = get_random_coordinates(self.length, self.height)
            # если в этой ячейки пустота -- то изменяем значение этой ячеки на бота
            #if str(self.board[x][y]) == '0':
            if self.board[x][y].value == 0:
                # меняем координаты у i-ого бота в списке bots
                self.bots[i].change_coordinates(x, y)

                # изменяет значение ячейки на '1'(бот)
                self.board[x][y].change_value(1)
                self.window.ui.ColorConfiguration(1, x, y, self.bots[i].health)  # <--
                # изменяет значение индекса ячейки на номер бота в списке
                self.board[x][y].change_index(i)
                i += 1


    # возвращает '0' -- если в координатах пусто, '1' -- бот, '2' -- еда, '3' -- яд, '4' -- стена
    def check_coordinates(self, x, y):
        return str(self.board[x][y])

    # x, y -- старые координаты бота, x1,y1 -- новые координаты бота, bot_number -- номер бота в списке bots
    def move_bot(self, x, y, x1, y1, bot_number):
        # меняем значение первой ячейки на 0
        self.board[x][y].change_value(0)
        self.window.ui.ColorConfiguration(0, x, y, 0)  # <--
        # меняем индекс первой ячейки на None
        self.board[x][y].change_index(None)
        # меняем значение второй ячейки на 1
        self.board[x1][y1].change_value(1)
        self.window.ui.ColorConfiguration(1, x1, y1, self.bots[bot_number].health)  # <--
        # меняем индекс второй ячейки на номер бота в массиве bots
        self.board[x1][y1].change_index(bot_number)

    def delete_food(self, x, y):
        # меняем значение ячейки с едой на 0
        self.board[x][y].change_value(0)
        self.window.ui.ColorConfiguration(0, x, y, 0)  # <--

    def poison_to_food(self, x, y):
        # меняем значение ячейки с ядом на 2
        self.board[x][y].change_value(2)
        self.window.ui.ColorConfiguration(2, x, y, 0)  # <--

    # удаляет бота из массива ботов и изменяет значение и индекс клетки, на которой стоял бот
    def delete_bot(self, bot_number):
        # print(str(bot_number) + " die")
        # меняем значение клетки, где стоял бот на 0
        self.board[self.bots[bot_number].x][self.bots[bot_number].y].change_value(0)
        self.window.ui.ColorConfiguration(0, self.bots[bot_number].x, self.bots[bot_number].y, 0)  # <--
        # меняем индекс клетки, где стоял бот на None
        self.board[self.bots[bot_number].x][self.bots[bot_number].y].change_index(None)
        # удаляем бота из масиива
        del self.bots[bot_number]

    # проверяет количетсво свободных клеток на арене
    def check_free(self):
        kol = 0
        # проходим по арене, прибавляем к kol еденицу, если клетка свободная
        for i in range(self.length):
            for j in range(self.height):
                if self.board[i][j].value == 0:
                    kol += 1
        return kol

    # генерирует на арене яд и еду
    def spawn_obj(self, obj, kol):
        if obj == "food":
            obj = 2
        elif obj == "poison":
            obj = 3
        else:
            obj = 0
        i = 0

        # если свободных меньше, чем нужно, то не спавним ничего
        if self.check_free() >= kol:
            # пока не заполним нужное количество ячеек
            while i < kol:
                # две рандомных координаты
                x, y = get_random_coordinates(self.length, self.height)

                # если в этой ячейки пустота -- то изменяем значение этой ячеки на obj
                if str(self.board[x][y]) == '0':
                    # изменяет значение ячейки на obj
                    self.board[x][y].change_value(obj)
                    i += 1
                    if not self.flag_skip:
                        self.window.ui.ColorConfiguration(obj, x, y, 0)  # <--


    # копируем ботов до количества count_of_bots -- делаем
    def copy_bots(self):
        # i ходит от 0 до количество ботов - сколько ботов уже есть в списке и т.к. у нас есть ещё вложенный цикл
        # делим на количество его операций
        for i in range((self.count_of_bots - self.end_count) // self.end_count):
            # проходим каждый раз по оставшимся ботам и делаем deepcopy каждого из них
            for j in range(self.end_count):
                self.bots.append(copy(self.bots[j]))

    # мутируем count_of_bots // end_count первых ботов, n -- сколько мутаций надо произвести
    def mutate_bots(self, n):
        # i принимает значения от 0 до number_mutation
        for i in range(self.number_mutation):
            # делаем мутацию у данного бота
            self.bots[i].mutate_bot(n)

    # чистит арену от яда, еды и ботов
    def clean_arena(self):
        # проходим по вертикалям
        for x in range(self.length):
            # проходим по каждой клетке
            for y in range(self.height):
                # если в клетке не стена и она не пуста
                if self.board[x][y].value != 4 and self.board[x][y].value != 0:
                    # меняем клетку на пустую
                    self.board[x][y].change_value(0)
                    if not self.flag_skip:
                        self.window.ui.ColorConfiguration(0, x, y, 0)

    #спавн ботов, еды и яда на арене
    def generation_start(self):
        self.spawn_obj("food", self.start_food)  # добавляем на арену еду
        self.spawn_obj("poison", self.start_poison)  # добавляем на арену яд
        self.make_bots()  # добавляем ботов на арену


    # точка вхождеия в симуляцию
    def move(self):
        # если ботов достаточно для продолжения и ход не закончен для каждого, то ход одного бота
        if self.bot_number < len(self.bots) and len(self.bots) > self.end_count:
            # запоминаем длинну массива bots
            length = len(self.bots)
            # оправляем номер бота в функцию start -- делает несколько ходов бота до заверщающего дейтсвия
            while not self.flag_finish:
                self.count_move += 1
                self.bots[self.bot_number].start(self)
            else:
                self.flag_finish = False
            # проверяем длинну массива bots, если она не изменилась(данный бот не умер), то идём по массиву дальше
            if length == len(self.bots):
                self.bot_number += 1
        else:
            self.bot_number = 0  # возвращаемся в начало
            # если ботов достаточно для продолжения
            if len(self.bots) > self.end_count:
                # спавним на арене яд
                self.spawn_obj("poison", 1)
                # спавним на арене еду
                self.spawn_obj("food", 1)

            # иначе конец поколения
            else:
                if not self.flag_skip:
                    self.window.ui.output.append(str(self.count_move))
                self.kol_of_move.append(self.count_move)
                if len(self.kol_of_move) % 100 == 0:
                    math_expr(self.kol_of_move)
                self.count_move = 0
                self.gen += 1
                # копируем ботов до изначального количества
                self.copy_bots()
                # делаем мутацию у ботов
                self.mutate_bots(self.genes_mutation)
                for i in range(len(self.bots)):
                    self.bots[i].health = 30
                # чистим арену от старых ботов, яда и еды
                self.clean_arena()
                # наша песня хороша - начинай сначала
                self.generation_start()
                # остановим таймер и будем ждать нажатия кнопки
                self.window.arena_startpause()

    def move_skip(self, skip):
        while self.gen < skip:
            self.move()
        else:
            self.gen = 0