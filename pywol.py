# pywol.py

import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from auth.authentication import AuthenticationManager

def main():
    app = QApplication(sys.argv)

    # Gestion de l'authentification
    auth_manager = AuthenticationManager()
    if not auth_manager.authenticate():
        sys.exit()

    # Initialisation de la fenêtre principale
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
