import json
import os
from PyQt5 import QtWidgets
from ui_score_window import Ui_Dialog

class ScoreWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # кнопка выхода
        self.ui.b_exit.clicked.connect(self.close)
        self.load_scores() #чтение json

    def set_score_text(self, text: str):
        self.ui.tb_score.setText(text)

    def load_scores(self):
        filename = "scores.json"
        if not os.path.exists(filename):
            self.ui.b_exit.setText("Результатов пока нет")
            return
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        lines = []
        for item in data:
            line = f"Имя: {item['player_name']}. Уровень: {item['level']}. Счет: {item['score']} "
            lines.append(line)

        self.ui.tb_score.setText("\n".join(lines))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    result_test = ScoreWindow()
    result_test.show()

    app.exec_()


