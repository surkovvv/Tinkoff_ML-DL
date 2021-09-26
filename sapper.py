import random

class Saper:
    def __init__(self, field_width=5, field_height=5, amount_of_bombs=3):
        self.field_width = field_width
        self.field_height = field_height
        self.amount_of_bombs = amount_of_bombs
        # -1 в player_field значит, что поле еще не открыли
        self.player_field = [[-1 for _ in range(self.field_width)] for _ in range(self.field_height)]
        # -1 в actual_field значит, что в этой ячейке стоит мина
        self.actual_field = [[0 for _ in range(self.field_width)] for _ in range(self.field_height)]

    def countBombsAround(self, row, column):
        counter = 0
        for r in range(-1, 2):
            for c in range(-1, 2):
                i = row + r
                j = column + c
                if i < 0 or j < 0 or i >= self.field_height or j >= self.field_width:
                    continue
                if self.actual_field[i][j] < 0:
                    counter += 1
        return counter

    def createField(self):
        """
        Первоначальная настройка игры
        :return:
        """
        rand_generator = random.Random()
        AoB = self.amount_of_bombs

        while AoB > 0:
            row = rand_generator.randrange(self.field_height)
            col = rand_generator.randrange(self.field_width)
            if self.actual_field[row][col] != 0:
                continue
            else :
                #print(self.actual_field[row][col])
                self.actual_field[row][col] = -1
                AoB -= 1

        for i in range(self.field_height):
            for j in range(self.field_width):
                if self.actual_field[i][j] == 0:
                    self.actual_field[i][j] = self.countBombsAround(i, j)

    def askInquiry(self):
        """
        Функция для обработки запроса игрока
        Доступные команды только Open и Flag
        Координаты вводятся от 1 до соотвествующих размеров
        :return: кортеж (command_id, row, column)
        """
        flag = True
        while flag:
            row, column, command = input("Введите координаты и команду через пробелы или введите команду 'Save _ _': ").split()
            if row == "Save":
                return (-1, 0, 0)
            if not row.isdigit():
                print("Неверный формат ввода координаты строки. Попробуйте еще раз:")
                continue
            elif int(row) < 1 or int(row) > self.field_height:
                print("Указанная строка выходит за рамки поля. Попробуйте еще раз:")
                continue

            if not column.isdigit():
                print("Неверный формат ввода координаты столбца. Попробуйте еще раз:")
                continue
            elif int(column) < 1 or int(column) > self.field_width:
                print("Указанный столбец выходит за рамки поля. Попробуйте еще раз:")
                continue
            row = int(row) - 1
            column = int(column) - 1

            if (command == "Flag"):
                return (0, row, column)
            elif (command == "Open"):
                return (1, row, column)
            else :
                print("Нет такой команды. Попробуйте еще раз:")
                continue


    def showField(self):
        """
        Функция для обновления поля в консоли
        Возможные значения ячеек нашего поля:
            ? - еще не открытое поле
            f - в этом поле поставили флаг
            * - бомба
            число - число бомб вокруг нашей ячейки
        :return:
        """
        for i in range(self.field_height):
            print("_" * 3 * self.field_width)
            for j in range(self.field_width):
                if self.player_field[i][j] == -1:
                    symb = '?'
                elif self.player_field[i][j] == 3:
                    symb = 'f'
                elif self.player_field[i][j] == 2:
                    symb = '*'
                else:
                    symb = str(self.actual_field[i][j])
                print(symb.center(3, '|'), end="")
            print()
        print("-" * 3 * self.field_width)

    def isFinished(self):
        """
        Функция определяет, завершилась ли игра:
        1) Игрок наступил на мину => завершаем игру как проигравший
        2) Игрок открыл все поля
        :return:
        -1, если игрок взорвался
        1, если игра продолжается
        -2, если игра завершилась, и игрок победил
        """
        for i in range(self.field_height):
            for j in range(self.field_width):
                if self.player_field[i][j] == 3 and self.actual_field[i][j] < 0:
                    continue
                elif self.player_field[i][j] != -1 and self.actual_field[i][j] < 0:
                    self.player_field[i][j] = 2
                    return -1
        for i in range(self.field_height):
            for j in range(self.field_width):
                if self.player_field[i][j] == -1 and self.actual_field[i][j] >= 0:
                    return 1
        return -2

    def start_game(self):
        """
        Функция запускает игру
        :return:
        """
        self.createField()
        #self.showField()
        finishFlag = 1
        while finishFlag > 0:
            self.showField()
            command, row, col = self.askInquiry()
            if (command == 0):
                self.player_field[row][col] = 3
            elif command == 1:
                self.player_field[row][col] = 0
            else:
                f = open('save.txt', 'w')
                for rows in self.player_field:
                    for symb in rows:
                        f.write(str(symb))
                    f.write('\n')
                f.close()
                print("Партия сохранена в файл save.txt")
                break;
            finishFlag = self.isFinished()
        self.showField()
        if finishFlag == -1:
            print("Вы проиграли")
        elif finishFlag == -2:
            print("Поздравляю! Вы победили.")


def playGame():
    while True:
        rows, columns, amount = input("Введите размеры поля и количество бомб через пробел:").split()
        rows, columns, amount = int(rows), int(columns), int(amount)
        game = Saper(rows, columns, amount)
        game.start_game()
        print("Начать заново?")
        answer = input("Введите 'да' или 'нет':")
        #print("Вы ввели", answer)
        if answer == "да":
            continue
        else:
            print("Спасибо за игру!")
            break

playGame()