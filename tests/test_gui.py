# tests/test_gui.py

import pytest
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

@pytest.fixture
def app(qtbot):
    test_app = QApplication([])
    main_window = MainWindow()
    qtbot.addWidget(main_window)
    return main_window

def test_main_window_title(app):
    assert app.windowTitle() == "PyWoL"
