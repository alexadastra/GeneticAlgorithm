from random import randint
from copy import deepcopy


class Bot:
    # создаём множества
    GO = {i for i in range(7)}  # движение (завершающее действие)
    SEIZE = {i for i in range(8, 15)}  # схватить еду или преобразовать яд в еду (завершающее действие)
    LOOK = {i for i in range(16, 23)}  # посмотреть
    TURN = {i for i in range(24, 31)}  # поворот

    def __init__(self, root_window, x=None, y=None):
        self.window = root_window
        super(Bot, self).__init__()
        self.view = randint(0, 3)  # зрение бота: 0 - вверх, 1 - вправо, 2 - вниз, 3 - влево
        self.health = 30  # здоровье бота

        self.memory = [randint(0, 63) for i in range(64)]  # мозг бота
        self.pointer = 0  # указатель на ячейку памяти в мозгу
        self.x = x  # координата x бота
        self.y = y  # координата y бота

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)

    def change_pointer(self, value):  # движение указателя в мозгу
        self.pointer += value
        if self.pointer > 63:
            self.pointer %= 64

    def change_coordinates(self, x, y):  # меняет координаты
        self.x = x
        self.y = y

    def change_health(self, value):  # меняет здоровье
        self.health += value

    # менет значение view
    def change_view(self, value):
        self.view += value
        if self.view > 3:
            self.view %= 4

    # координаты в зависимости от запроса, взгляда и положения бота
    # value -- memory[pointer]
    def look(self, value, view, x, y):
        value += view * 2
        if value > 7:
            value %= 8

        if value == 0:
            y += 1
        elif value == 1:
            x += 1
            y += 1
        elif value == 2:
            x += 1
        elif value == 3:
            x += 1
            y -= 1
        elif value == 4:
            y -= 1
        elif value == 5:
            x -= 1
            y -= 1
        elif value == 6:
            x -= 1
        else:
            x -= 1
            y += 1
        return x, y

    # в зависимости от значения ячейки двигает указатель
    # value -- значение ячейки
    def move_pointer(self, value):
        # яд
        if value == 3:
            self.change_pointer(1)
        # стена
        elif value == 4:
            self.change_pointer(2)
        # бот
        elif value == 1:
            self.change_pointer(3)
        # еда
        elif value == 2:
            self.change_pointer(4)
        # пусто
        else:
            self.change_pointer(5)

    # bot_number -- номер бота в массиве bots
    def start(self, arena):
            # если клетка памяти бота -- это "ходить"
            if self.memory[self.pointer] in self.GO:
                # x1, y1 -- координаты, на которые надо сходить
                x1, y1 = self.look(self.memory[self.pointer], self.view, self.x, self.y)
                # если новые координаты находятся на арене
                if x1 >= 0 and y1 >= 0 and x1 < arena.length and y1 < arena.height:
                    # print("GO")
                    # если на координаты, куда нам нужно сходить пустота -- то ходим
                    if arena.check_coordinates(x1, y1) == '0':
                        # меняем координаты у ячейки в арене
                        arena.move_bot(self.x, self.y, x1, y1, arena.bot_number)
                        # меняем координаты в самом боте
                        self.change_coordinates(x1, y1)
                    # если еда -- то ходим и пополняем здоровье
                    elif arena.check_coordinates(x1, y1) == '2':
                        # меняем координаты у ячейки в арене
                        arena.move_bot(self.x, self.y, x1, y1, arena.bot_number)
                        # меняем координаты в самом боте
                        self.change_coordinates(x1, y1)
                        # увеличиваем здоровье
                        self.change_health(10)
                        if not arena.flag_skip:
                            self.window.ColorConfiguration(1, self.x, self.y, self.health)  # <--
                    # если яд -- то ходим и убавляем здоровье бота
                    elif arena.check_coordinates(x1, y1) == '3':
                        # меняем координаты у ячейки в арене
                        arena.move_bot(self.x, self.y, x1, y1, arena.bot_number)
                        # меняем координаты в самом боте
                        self.change_coordinates(x1, y1)
                        # убиваем бота
                        self.change_health(-15)
                        if not arena.flag_skip:
                            self.window.ColorConfiguration(1, self.x, self.y, self.health)
                    # если бот или стена, то не ходим

                    # перемещаем указатель в голове у бота
                    # int(arena.check_coordinates(x1, y1)) -- проверяем, что находится в этой ячейке
                    self.move_pointer(int(arena.check_coordinates(x1, y1)))
                    arena.flag_finish = True  # так как перемещение бота -- завершающее действие

            # если клетка памяти бота -- это "схватить еду или преобразовать яд в еду"
            elif self.memory[self.pointer] in self.SEIZE:
                # x1, y1 -- координаты, на которые надо посмотреть и найти еду или яд
                x1, y1 = self.look(self.memory[self.pointer], self.view, self.x, self.y)
                # если новые координаты находятся на арене
                if 0 <= x1 < arena.length and 0 <= y1 < arena.height:
                    # print("SEIZE")
                    # если еда -- то кушаем её
                    if arena.check_coordinates(x1, y1) == '2':
                        # меняем значение у ячейки в арене
                        arena.delete_food(x1, y1)
                        # увеличиваем здоровье бота
                        self.change_health(10)
                        if not arena.flag_skip:
                            self.window.ColorConfiguration(1, self.x, self.y, self.health)  # <--
                    elif arena.check_coordinates(x1, y1) == '3':
                        # меняем значение у ячейки в арене
                        arena.poison_to_food(x1, y1)
                    # если пустота, бот или стена, то не ходим

                    # перемещаем указатель в голове у бота
                    # int(arena.check_coordinates(x1, y1)) -- проверяем, что находится в этой ячейке
                    self.move_pointer(int(arena.check_coordinates(x1, y1)))
                    arena.flag_finish = True  # так как -- завершающее действие

            # если клетка памяти бота -- это "смотреть"
            elif self.memory[self.pointer] in self.LOOK:
                # print("LOOK")
                # x1, y1 -- координаты, на которые надо посмотреть
                x1, y1 = self.look(self.memory[self.pointer], self.view, self.x, self.y)
                # если новые координаты находятся на арене
                if x1 >= 0 and y1 >= 0 and x1 < arena.length and y1 < arena.height:
                    # перемещаем указатель в голове у бота
                    # int(arena.check_coordinates(x1, y1)) -- проверяем, что находится в этой ячейке
                    self.move_pointer(int(arena.check_coordinates(x1, y1)))

            # если клетка памяти бота -- это "повернуть"
            elif self.memory[self.pointer] in self.TURN:
                # print("TURN")
                # обозначим значение в памяти, на которое указывает poiter за value
                value = self.memory[self.pointer]
                # меняем взгляд бота в зависимости от значения
                if value in (24, 25):
                    self.change_view(1)
                elif value in (26, 27):
                    self.change_view(2)
                elif value in (28, 29):
                    self.change_view(3)

                # перемещаем указатель в голове у бота
                self.change_pointer(1)

            # если клетка памяти бота -- это "безусловный переход"
            else:
                # перемещаем pointer на значение, которое было в памяти у бота
                self.change_pointer(self.memory[self.pointer])

            # после каждого хода уменьшаем здоровье бота на 1 еденицу
            self.health -= 1
            if not arena.flag_skip:
                self.window.ColorConfiguration(1, self.x, self.y, self.health)

            # если здоровье бота меньше 1, то убиваем его
            if self.health < 1:
                arena.flag_finish = True
                arena.delete_bot(arena.bot_number)

    # мутирование бота, n -- количество мутаций, которое надо произвести
    def mutate_bot(self, n):
        # значение ячейки памяти от рандомного числа от 0 до 63 меняем на рандомное число от 0 до 63 n раз
        for i in range(n):
            self.memory[randint(0, 63)] = randint(0, 63)
