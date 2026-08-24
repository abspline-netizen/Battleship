from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from ui_mainwindow import Ui_MainWindow
from settings_window import SettingsWindow
from new_game_window import NewGameWindow
from controller import GameController
from score_window import ScoreWindow
import sys
import os
import json
# from logging_config import setup_logging_debug
# import logging
# logger = logging.getLogger(__name__)


class MainWindow(QtWidgets.QMainWindow):
    SETTINGS_FILE = "settings.json"
    COLOR_MAP = {
        "Синий": "blue",
        "Зелёный": "green",
        "Красный": "red",
        "Серый": "gray",
        "Тёмный": "navy",
        "Светлый": "lightgray"
    }

    def __init__(self):
        # logger.debug("====== Старт main.py ======")
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.controller = GameController(self)

        self.ui.verticalLayout_2.setStretch(0, 0)  # верхний пустой widget
        self.ui.verticalLayout_2.setStretch(1, 0)  # лейбл Компьютер
        self.ui.verticalLayout_2.setStretch(2, 1)  # поле компьютера
        self.ui.verticalLayout_2.setStretch(3, 0)  # Ход компьютера

        self.ui.verticalLayout.setStretch(0, 0)
        self.ui.verticalLayout.setStretch(1, 0)
        self.ui.verticalLayout.setStretch(2, 1)
        self.ui.verticalLayout.setStretch(3, 0)

        self.field_size = 350  # фиксированный размер поля

        # фиксируем размер фреймов
        self.ui.player_fild.setFixedSize(self.field_size + 30, self.field_size + 30)
        self.ui.frame_computer_fild.setFixedSize(self.field_size + 30, self.field_size + 30)

        # создаём лейауты для полей
        player_layout = QtWidgets.QGridLayout()
        computer_layout = QtWidgets.QGridLayout()

        self.ui.verticalLayout_3.addLayout(player_layout)
        self.ui.verticalLayout_4.addLayout(computer_layout)

        self.settings = self.load_settings()
        self.field_size = self.settings["field_size"]

        # --- фиксируем размер фреймов ---
        self.ui.player_fild.setFixedSize(self.field_size + 30, self.field_size + 30)
        self.ui.frame_computer_fild.setFixedSize(self.field_size + 30, self.field_size + 30)

        self.create_player_field()
        self.create_computer_field()

        self.apply_ship_colors()
        self.apply_font_size(self.settings["font_size"])

        #кнопка настройки
        self.ui.b_settings.clicked.connect(self.open_settings)
        #кнопка новая игра
        self.ui.b_new_game.clicked.connect(self.open_new_game)

        # logger.debug("MainWindow начальная инициализация переменных")# если это QDialog

    def open_new_game(self):
        new_game = NewGameWindow(self)
        new_game.exec_()
        # logger.debug("MainWindow - open_new_game")

    def open_settings(self):
        settings = SettingsWindow(self)
        settings.exec_()   # для диалога

    def clear_layout(self, layout): #очищаются layout для изменения размеров поля
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def create_player_field(self):
        layout = self.ui.verticalLayout_3   # используем существующий layout
        self.player_buttons = []

        # очищаем layout от тестовых кнопок
        self.clear_layout(layout)
        # создаём сетку внутри существующего layout
        grid = QtWidgets.QGridLayout()
        layout.addLayout(grid)

        for row in range(10):
            row_buttons = []
            for col in range(10):
                btn = QtWidgets.QPushButton("")
                btn.setFixedSize( (self.field_size-50)//10, (self.field_size-50)//10 )
                btn.setStyleSheet("background-color: lightblue;")
                grid.addWidget(btn, row, col)
                row_buttons.append(btn)

            self.player_buttons.append(row_buttons)
        # logger.debug(f"MainWindow - create_player_field - self.player_buttons = {self.player_buttons}")

    def create_computer_field(self):
        layout = self.ui.verticalLayout_4   # используем существующий layout
        self.computer_buttons = []

        # очищаем layout от тестовых кнопок
        self.clear_layout(layout)

        # создаём сетку внутри существующего layout
        grid = QtWidgets.QGridLayout()
        layout.addLayout(grid)

        for row in range(10):
            row_buttons = []
            for col in range(10):
                btn = QtWidgets.QPushButton("")
                btn.setFixedSize((self.field_size-50)//10, (self.field_size-50)//10)
                btn.setStyleSheet("background-color: lightgray;")
                grid.addWidget(btn, row, col)
                row_buttons.append(btn)

                btn.clicked.connect(lambda _, r=row, c=col: self.controller.player_click(r, c))

            self.computer_buttons.append(row_buttons)
        # logger.debug(f"MainWindow - create_computer_field - self.player_buttons = {self.computer_buttons}")

    def show_player_ships(self, field):
        for row in range(10):
            for col in range(10):
                if field[row][col] == 1:  # корабль
                    btn = self.player_buttons[row][col]
                    btn.setStyleSheet("background-color: navy;")  # цвет корабля

    def update_time(self, time_left):
        self.ui.lcd_timer.display(time_left)

    def update_event(self, text):
        self.ui.l_score_change.setText(text)

    def update_computer_field(self, x, y, hit):
        btn = self.computer_buttons[x][y]

        if hit:
            computer_ship = self.COLOR_MAP[self.settings["computer_ship_color"]]
            btn.setStyleSheet(f"background-color: {computer_ship};")
        else:
            btn.setStyleSheet("background-color: white;")
            self.update_event(f"Промах! -{self.controller.game.penalty_time} сек")

        btn.setEnabled(False)
        self.update_time(self.controller.game.time_left)
        # logger.debug(f"MainWindow - update_computer_field")

    def update_player_field(self, x, y, hit):
        btn = self.player_buttons[x][y]

        if hit:
            btn.setStyleSheet("background-color: red;")
            self.update_event("Компьютер попал!")
        else:
            btn.setStyleSheet("background-color: white;")
            # self.update_event("Компьютер промахнулся")

        self.update_time(self.controller.game.time_left)
        # logger.debug(f"MainWindow - update_computer_field")

    def reset_fields(self):
        self.create_player_field()
        self.create_computer_field()
        self.update_event("Игра началась")
        self.update_time(self.controller.game.time_left)

    def show_score(self, score_value):
        score = ScoreWindow(self)
        score.set_score_text(str(score_value))   # преобразуем в строку внутри UI
        score.exec_()

    def disable_fields(self):
        for row in self.player_buttons:
            for btn in row:
                btn.setEnabled(False)

        for row in self.computer_buttons:
            for btn in row:
                btn.setEnabled(False)

    def show_message(self, text):
        QMessageBox.information(self, "Результат игры", text)

    def show_player_turn(self):
        self.ui.label_player_move.setStyleSheet("color: black; font-weight: bold;")
        self.ui.label_computer_move.setStyleSheet("color: gray;")

    def show_computer_turn(self):
        self.ui.label_player_move.setStyleSheet("color: gray;")
        self.ui.label_computer_move.setStyleSheet("color: black; font-weight: bold;")

    def set_player_name(self, name):
        self.ui.l_gamer.setText(name)

# чтение и запить в json
    def load_settings(self):
        if not os.path.exists(self.SETTINGS_FILE):
            return {
                    "font_size": 12,
                    "player_ship_color": "Синий",
                    "player_field_color": "Синий",
                    "computer_field_color": "Тёмный",
                    "computer_ship_color": "Светлый",
                    "field_size": 350
                   }

        with open(self.SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_settings(self, settings: dict):
    # Сохраняет настройки в JSON
        with open(self.SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)

    def apply_font_size(self, size):
        style = f"font-size: {size}px;"

        # Лейблы хода
        self.ui.label_player_move.setStyleSheet(style)
        self.ui.label_computer_move.setStyleSheet(style)

        # Имя игрока
        self.ui.l_gamer.setStyleSheet(style)
        self.ui.label_computer.setStyleSheet(style)

        # Таймер
        self.ui.lcd_timer.setStyleSheet(style)

        # События
        self.ui.l_score_change.setStyleSheet(style)

        # Кнопки полей
        for row in self.player_buttons:
            for btn in row:
                btn.setStyleSheet(style)

        for row in self.computer_buttons:
            for btn in row:
                btn.setStyleSheet(style)

    def apply_ship_colors(self):
        if not self.controller.game:
            return

        # CSS цвета
        player_ship = self.COLOR_MAP[self.settings["player_ship_color"]]
        player_field = self.COLOR_MAP[self.settings["player_field_color"]]
        computer_field = self.COLOR_MAP[self.settings["computer_field_color"]]
        computer_ship = self.COLOR_MAP[self.settings["computer_ship_color"]]

        #поле игрока
        for row in self.player_buttons:
            for btn in row:
                btn.setStyleSheet(f"background-color: {player_field};")

        #поле компьютера
        for row in self.computer_buttons:
            for btn in row:
                btn.setStyleSheet(f"background-color: {computer_field};")

        #корабли игрока
        if self.controller.game:
            field = self.controller.game.player_field
            for r in range(10):
                for c in range(10):
                    if field[r][c] == 1:
                        self.player_buttons[r][c].setStyleSheet(f"background-color: {player_ship};")

        #цвет попадания
        if self.controller.game:
            field = self.controller.game.computer_field
            for r in range(10):
                for c in range(10):
                    if field[r][c] == 3:
                        self.computer_buttons[r][c].setStyleSheet(f"background-color: {computer_ship};")

# !!!!!!!!! подсветка созданных кораблей компьютера - закрыть веред релизом
        # if self.controller.game:
        #     field = self.controller.game.computer_field
        #     for r in range(10):
        #         for c in range(10):
        #             if field[r][c] == 1:
        #                 self.computer_buttons[r][c].setStyleSheet(f"background-color: yellow;")

    def apply_field_size(self, size):
        self.field_size = size

        # обновляем фиксированные размеры фреймов
        self.ui.player_fild.setFixedSize(self.field_size + 30, self.field_size + 30)
        self.ui.frame_computer_fild.setFixedSize(self.field_size + 30, self.field_size + 30)

        # очищаем старые layout-ы
        self.clear_layout(self.ui.verticalLayout_3)
        self.clear_layout(self.ui.verticalLayout_4)

        # пересоздаём поля
        self.create_player_field()
        self.create_computer_field()
        self.apply_ship_colors()

if __name__ == "__main__":
    # setup_logging_debug()
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    QtCore.QTimer.singleShot(0, window.open_new_game)
    sys.exit(app.exec_())
