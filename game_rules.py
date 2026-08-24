from PyQt5 import QtWidgets
from ui_game_rules import Ui_Dialog

class RulesWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # кнопка прочитано == ок
        self.ui.b_ok.clicked.connect(self.close)