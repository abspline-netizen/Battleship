from PyQt5 import QtWidgets
from ui_new_game import Ui_Dialog
from score_window import ScoreWindow
from game_rules import RulesWindow
from logging_config import setup_logging_debug
# import logging
# logger = logging.getLogger(__name__)


class NewGameWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        #кнопка окно результатов
        self.ui.b_all_results.clicked.connect(self.open_score_window)
        #кнопка правила игры
        self.ui.b_rules.clicked.connect(self.open_rules_window)
        # кнопка начала игры
        self.ui.b_start_game.clicked.connect(self.start_game)
        # кнопка выход
        self.ui.b_cancel.clicked.connect(self.close)
        # logger.debug("NewGameWindow начальная инициализация переменных")

    def start_game(self):
        index = self.ui.cb_level.currentIndex()

        if index == 0:
            level = "easy"
        elif index == 1:
            level = "medium"
        elif index == 2:
            level = "hard"

        # logger.debug(f"NewGameWindow - start_game - index = {index}, level = {level}")
        player_name = self.ui.lineEdit.text()
        # logger.debug(f"NewGameWindow - start_game - player_name = {player_name}")
        self.parent().controller.start_new_game(level, player_name)
        # logger.debug(f"NewGameWindow - start_game - parent() - level = {level}, player_name = {player_name} ")
        self.close()



    def open_score_window(self):
        score_window = ScoreWindow(self)
        score_window.exec_()   # если это QDialog


    def open_rules_window(self):
        rules_window = RulesWindow(self)
        rules_window.exec_()

