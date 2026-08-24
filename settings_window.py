from PyQt5 import QtWidgets
from ui_settings import Ui_Dialog   # имя класса зависит от твоего .ui

class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.parent = parent  # MainWindow
        self.settings = parent.settings.copy()

        self.ui.spinBox_font_3.setValue(self.settings["font_size"])
        self.ui.cb_color_fild_player_2.setCurrentText(self.settings["player_ship_color"])
        self.ui.cb_color_fild_player.setCurrentText(self.settings["player_field_color"])
        self.ui.cb_color_fild_player_3.setCurrentText(self.settings["computer_field_color"])
        self.ui.cb_color_fild_player_4.setCurrentText(self.settings["computer_ship_color"])
        self.ui.spinBox_fild_size.setValue(self.settings["field_size"])

        # Подключаем сигналы
        self.ui.spinBox_font_3.valueChanged.connect(self.change_font_size)
        self.ui.cb_color_fild_player_2.currentTextChanged.connect(self.change_player_ship_color)
        self.ui.cb_color_fild_player.currentTextChanged.connect(self.change_player_field_color)
        self.ui.cb_color_fild_player_3.currentTextChanged.connect(self.change_computer_field_color)
        self.ui.cb_color_fild_player_4.currentTextChanged.connect(self.change_computer_ship_color)
        self.ui.spinBox_fild_size.valueChanged.connect(self.change_field_size)

        self.ui.b_to_default.clicked.connect(self.reset_defaults)

        # OK применяем настройки
        self.ui.buttonBox.accepted.connect(self.apply_all_settings)

    def change_font_size(self, value):
        self.settings["font_size"] = value


    def change_player_ship_color(self, value):
        self.settings["player_ship_color"] = value


    def change_player_field_color(self, value):
        self.settings["player_field_color"] = value


    def change_computer_field_color(self, value):
        self.settings["computer_field_color"] = value


    def change_computer_ship_color(self, value):
        self.settings["computer_ship_color"] = value


    def change_field_size(self, value):
        self.settings["field_size"] = value


    def apply_all_settings(self):
        # сохраняем
        self.parent.settings.update(self.settings)
        self.parent.save_settings(self.parent.settings)
        # применяем
        self.parent.apply_font_size(self.settings["font_size"])
        self.parent.apply_ship_colors()
        self.parent.apply_field_size(self.settings["field_size"])

    def reset_defaults(self):
        defaults = {
            "font_size": 12,
            "player_ship_color": "Синий",
            "player_field_color": "Светлый",
            "computer_field_color": "Светлый",
            "computer_ship_color": "Красный", #цвет подбитого корабля
            "field_size": 350
        }
# #   COLOR_MAP = {
#         "Синий": "blue",
#         "Зелёный": "green",
#         "Красный": "red",
#         "Серый": "gray",
#         "Тёмный": "navy",
#         "Светлый": "lightgray"
#     }
        self.settings.update(defaults)
        self.parent.save_settings(self.settings)

        # Обновляем UI
        self.ui.spinBox_font_3.setValue(defaults["font_size"])
        self.ui.cb_color_fild_player_2.setCurrentText(defaults["player_ship_color"])
        self.ui.cb_color_fild_player.setCurrentText(defaults["player_field_color"])
        self.ui.cb_color_fild_player_3.setCurrentText(defaults["computer_field_color"])
        self.ui.cb_color_fild_player_4.setCurrentText(defaults["computer_ship_color"])
        self.ui.spinBox_fild_size.setValue(defaults["field_size"])

        # Применяем
        self.parent.apply_font_size(defaults["font_size"])
        self.parent.apply_ship_colors()
        self.parent.apply_field_size(defaults["field_size"])
