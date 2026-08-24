from game_model import GameGear
from PyQt5.QtCore import QTimer
from logging_config import setup_logging_debug
import json
import os
import logging
logger = logging.getLogger(__name__)

class GameController:
    # def __init__(self):
    def __init__(self, main_window):
        self.main = main_window
        self.game = None


        logger.debug("GameController - инициализация")

    def start_new_game(self, level, player_name):
        #создаеться поля и корабли игрока и компьютера, таймер.
        if self.game is not None: #  остановить старый таймер
            self.game.stop_timer = True


        self.player_name = player_name
        self.main.set_player_name(player_name)
        self.game = GameGear(level)
        self.main.reset_fields()
        self.main.update_time(self.game.time_left)
        self.main.show_player_ships(self.game.player_field)
        self.main.apply_ship_colors()
        self.game.on_time_change = self.update_time_from_model


    def update_time_from_model(self, time_left):
        if time_left<0:
            time_left = 0
        self.main.update_time(time_left)

    def player_click(self, x, y):

        hit = self.game.player_move(x, y)
        # print(f'player hit = {hit}')
        # обновляем поле компьютера
        self.main.update_computer_field(x, y, hit)

        if self.game.game_over: #если игра закончилась, запусти give_in
            self.give_in(None)
            return

        if hit: #попал - поле изменилось
            return
        else:
            to_next = "computer"
            self.give_in(to_next) #передай ход

    def computer_clic(self):

        row, col, hit = self.game.computer_move()
        # print(f'computer hit = {hit}')
        self.main.update_player_field(row, col, hit)

        if self.game.game_over:
            self.give_in(None)
            return

        if hit:
            to_next = "computer"
            self.give_in(to_next) #передай ход
        else:
            to_next = "player"
            self.give_in(to_next) #передай ход

    def give_in(self, to_next): #передает очередность ходов
        if self.game.game_over: #проверка окончания игры
            logger.debug(f"GameController - game_over - {self.game.game_over}")

            # если игрок выиграл → сохраняем результат
            if self.game.winner == "player":
                logger.debug(f"GameController - self.game.winner == player - {self.game.winner}")
                score = self.game.get_final_score()
                self.main.show_message(f"{self.player_name} выиграл! Счет: {score}")
                logger.debug(f"GameController - self.main.show_message r - {self.main.show_message}")
                self.save_score()

            # если компьютер выиграл → выводим сообщение
            if self.game.winner == "computer":
                self.main.show_message("Компьютер выиграл!")


            # заблокировать поля
            self.main.disable_fields()
            # открыть окно новой игры
            self.main.open_new_game()
            return

        if to_next == "computer":
            self.main.show_computer_turn()
            QTimer.singleShot(500, self.computer_clic)

        elif to_next == "player":
            self.main.show_player_turn()

            pass

    def save_score(self):
        result = {
            "player_name": self.player_name,
            "level": self.game.level,
            "score": self.game.get_final_score()

        }

        filename = "scores.json"

        # если файла нет — создаём пустой список
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        # читаем существующие результаты
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # добавляем новый результат
        data.append(result)

        # сохраняем обратно
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    pass


