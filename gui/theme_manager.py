# gui/theme_manager.py

from PySide6.QtCore import QObject
from database.settings_manager import SettingsManager

class ThemeManager(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_manager = SettingsManager()

    def get_theme(self):
        return self.settings_manager.get_theme() or 'light'

    def get_accent_color(self):
        return self.settings_manager.get_setting('accent_color') or '#4CAF50'  # Couleur par défaut

    def get_stylesheet(self):
        theme = self.get_theme()
        accent_color = self.get_accent_color()

        if theme == 'dark':
            return f"""
                /* Styles généraux pour le thème sombre */
                QWidget {{
                    background-color: #2b2b2b;
                    color: #ffffff;
                }}
                QPushButton {{
                    background-color: {accent_color};
                    color: #ffffff;
                    border: none;
                    padding: 5px;
                    border-radius: 5px;
                }}
                QPushButton:hover {{
                    background-color: {accent_color};
                    opacity: 0.8;
                }}
                QLabel {{
                    color: #ffffff;
                }}

                /* Styles pour la barre de titre personnalisée */
                QWidget#title_bar {{
                    background-color: #1c1c1c;
                    border-bottom: 1px solid #444444;
                }}
                QLabel#title_label {{
                    color: #ffffff;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 5px;
                }}
                QPushButton#minimize_button, QPushButton#maximize_button, QPushButton#close_button {{
                    background-color: transparent;
                    border: none;
                    color: {accent_color};
                    font-size: 14px;
                    padding: 5px;
                }}
                QPushButton#minimize_button:hover, QPushButton#maximize_button:hover {{
                    background-color: #444444;
                }}
                QPushButton#close_button:hover {{
                    background-color: #c0392b;
                }}
                QListWidget {{
                    border: 1px solid {accent_color};
                }}
            """
        else:
            return f"""
                /* Styles généraux pour le thème clair */
                QWidget {{
                    background-color: #f0f0f0;
                    color: #000000;
                }}
                QPushButton {{
                    background-color: {accent_color};
                    color: #ffffff;
                    border: none;
                    padding: 5px;
                    border-radius: 5px;
                }}
                QPushButton:hover {{
                    background-color: {accent_color};
                    opacity: 0.8;
                }}
                QLabel {{
                    color: #000000;
                }}

                /* Styles pour la barre de titre personnalisée */
                QWidget#title_bar {{
                    background-color: #e0e0e0;
                    border-bottom: 1px solid #cccccc;
                }}
                QLabel#title_label {{
                    color: #000000;
                    font-weight: bold;
                    font-size: 16px;
                    padding: 5px;
                }}
                QPushButton#minimize_button, QPushButton#maximize_button, QPushButton#close_button {{
                    background-color: transparent;
                    border: none;
                    color: {accent_color};
                    font-size: 14px;
                    padding: 5px;
                }}
                QPushButton#minimize_button:hover, QPushButton#maximize_button:hover {{
                    background-color: #cccccc;
                }}
                QPushButton#close_button:hover {{
                    background-color: #e74c3c;
                }}
                QListWidget {{
                    border: 1px solid {accent_color};
                }}
            """

    def set_theme(self, theme):
        self.settings_manager.set_theme(theme)
