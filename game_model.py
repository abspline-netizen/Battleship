import random
import threading
import time
from logging_config import setup_logging_debug
# import logging
import time
# logger = logging.getLogger(__name__)

class GameGear:
    def __init__(self, level = "easy"):

        self.size = 10 #10x10

        self.time_left = 200
        self.streak_hits = 0 #серия попаданий
        self.bonus_time = 0

        self.penalty_time = 0
        self.on_time_change = None #передаем в контроллер
        #уровень сложности
        self.level = level
        self.set_level()

        #создаем поле боя
        self.computer_field = self.generate_field()
        self.computer_field = self.generate_fleet(self.computer_field)

        self.player_field = self.generate_field()
        self.player_field = self.generate_fleet(self.player_field)

        self.computer_shots = set() #хранение выстрелов компьютера
        self.winner = None #кто победил
        self.game_over = False
        self.stop_timer = False #флаг остановки таймера
        self.countdown()

        # logger.debug("GameGear начальная инициализация переменных")

        #настроить уровень сложности
    def set_level(self):
        if self.level == "easy": #легкий уровень
            self.bonus_time = 10
            self.penalty_time = 4
        elif self.level == "medium": #средний уровень
            self.bonus_time = 5
            self.penalty_time = 3
        elif self.level == "hard": #трудный уровень
            self.bonus_time = 3
            self.penalty_time = 5

        #Генератор поля
    def generate_field(self):
        gen_field = [[0]*10 for _ in range(10)]
        return gen_field

    def ship_in_field(self, field, ship_size=4, need_ship=1):
        count_ship = 0

        while count_ship < need_ship:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            orientation = random.choice(["horizontal", "vertical"])

            # Проверка, что корабль целиком в поле
            if orientation == "horizontal":
                if col + ship_size > self.size:
                    continue
                if any(field[row][col + i] != 0 for i in range(ship_size)):
                    continue
            else:  # vertical
                if row + ship_size > self.size:
                    continue
                if any(field[row + j][col] != 0 for j in range(ship_size)):
                    continue

            # Размещение корабля (единицы)
            if orientation == "horizontal":
                for i in range(ship_size):
                    field[row][col + i] = 1

                # Обводка двойками с проверкой границ
                for i in range(-1, ship_size + 1):
                    if 0 <= row - 1 < self.size and 0 <= col + i < self.size:
                        field[row - 1][col + i] = 2
                    if 0 <= row + 1 < self.size and 0 <= col + i < self.size:
                        field[row + 1][col + i] = 2

                if 0 <= row < self.size and 0 <= col - 1 < self.size:
                    field[row][col - 1] = 2
                if 0 <= row < self.size and 0 <= col + ship_size < self.size:
                    field[row][col + ship_size] = 2

            else:  # vertical
                for j in range(ship_size):
                    field[row + j][col] = 1

                # слева
                if col - 1 >= 0:
                    for j in range(ship_size):
                        if 0 <= row + j < self.size and 0 <= col - 1 < self.size:
                            field[row + j][col - 1] = 2
                # справа
                if col + 1 < self.size:
                    for j in range(ship_size):
                        if 0 <= row + j < self.size and 0 <= col + 1 < self.size:
                            field[row + j][col + 1] = 2
                # сверху delta column
                if row - 1 >= 0:
                    for dc in (-1, 0, 1):
                        if 0 <= row - 1 < self.size and 0 <= col + dc < self.size:
                            field[row - 1][col + dc] = 2
                # снизу
                if row + ship_size < self.size:
                    for dc in (-1, 0, 1):
                        if 0 <= row + ship_size < self.size and 0 <= col + dc < self.size:
                            field[row + ship_size][col + dc] = 2

            count_ship += 1

        return field

        # Генерация флота
    def generate_fleet(self, field):

        #создаем корабли на поле, поле каждый раз перезаписывается в новом состоянии
        four_deck = self.ship_in_field(field, ship_size = 4, need_ship = 1)
        three_deck = self.ship_in_field(four_deck, ship_size = 3, need_ship = 2)
        two_deck = self.ship_in_field(three_deck, ship_size = 2, need_ship = 3)
        one_deck = self.ship_in_field(two_deck, ship_size = 1, need_ship = 4)

        print("===Положения кораблей===") #для проверки
        print(f"one_deck 0 = {one_deck[0]}")
        print(f"one_deck 1 = {one_deck[1]}")
        print(f"one_deck 2 = {one_deck[2]}")
        print(f"one_deck 3 = {one_deck[3]}")
        print(f"one_deck 4 = {one_deck[4]}")
        print(f"one_deck 5 = {one_deck[5]}")
        print(f"one_deck 6 = {one_deck[6]}")
        print(f"one_deck 7 = {one_deck[7]}")
        print(f"one_deck 8 = {one_deck[8]}")
        print(f"one_deck 9 = {one_deck[9]}")
        return one_deck

    def player_move(self, press_button_row, press_button_col): #made_fleet - list in list, ходит по полю компьютера
        hit = False
        if self.computer_field[press_button_row][press_button_col]== 1: #если попал в корабль, перезаписываем значение поля в подбитые корабли
            self.computer_field[press_button_row][press_button_col] = 3
            self.streak_hits += 1
            bonus = self.bonus_time * self.streak_hits #учитываеться серия попаданий
            self.time_left += bonus #прибавляеться время
            hit = True # флаг попадания
            # print(f'make_move - self.computer_fild {self.computer_field}')

        else: #промахнулся - время отнимается
            self.time_left -= self.penalty_time
            self.streak_hits = 0

        self.game_over_check()
        return hit

    def computer_move(self):
        hit = False
        while True:
            row = random.randint(0, self.size -1)
            col = random.randint(0, self.size -1)
            tuple_coordinate = (row, col)
            # print(f'player_fild = {self.player_fild}')
            if not tuple_coordinate in self.computer_shots:
                self.computer_shots.add(tuple_coordinate)
                if self.player_field[row][col] == 1: #если попал в корабль
                    self.player_field[row][col] = 3 #тогда переведи его в состояние подбитых
                    hit = True
                self.game_over_check()
                # print(f'computer_shots =  {self.computer_shots}')
                return row, col, hit

    def game_over_check(self):
        # время вышло =компьютер победил
        if self.time_left <= 0:
            self.game_over = True
            self.winner = "computer"
            return

        # нет кораблей у игрока = компьютер победил
        if not any(1 in row for row in self.player_field):
            self.game_over = True
            self.winner = "computer"
            return

        # нет кораблей у компьютера =игрок победил
        if not any(1 in row for row in self.computer_field):
            self.game_over = True
            self.winner = "player"
            return

        # иначе игра продолжается
        self.game_over = False

    def countdown(self): #обратный отсчет по таймеру в параллельном потоке
        thread = threading.Thread(target = self.timer)
        thread.daemon = True
        thread.start()

    def timer(self):
        while self.time_left>0 and not self.game_over and not self.stop_timer:
            time.sleep(1)
            self.time_left -= 1

            if self.on_time_change:
                self.on_time_change(self.time_left)

            self.game_over_check()

        if self.time_left<=0:
            self.time_left = 0
            if self.on_time_change:
                self.on_time_change(self.time_left)

    def get_final_score(self): #получение итогового счета
        if not self.game_over:
            return None
        return max(self.time_left, 0)

if __name__ == "__main__":
    # pass
    # setup_logging_debug()
    print("== Test class GameGear ==")
    my_test_app = GameGear(level = "easy")

    comp_field = my_test_app.generate_field()
    comp_fleet = my_test_app.generate_fleet(comp_field )

    player_field = my_test_app.generate_field()
    player_fleet = my_test_app.generate_fleet(player_field)

    print(f'comp_fleet = {comp_fleet}')
    print(f'player_fleet = {player_fleet}')




