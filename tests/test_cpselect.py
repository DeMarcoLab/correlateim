import sys

import numpy as np
import pytest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog

from correlateim import cpselect


@pytest.fixture
def window(qtbot):
    """Pass the application to the test functions via a pytest fixture."""
    img1 = np.random.random((500, 500))
    img2 = np.random.random((500, 500))
    app = QApplication(sys.argv)
    window = cpselect._MainWindow(img1, img2)
    qtbot.add_widget(window)
    window.show()
    return window


def test_window_title(window):
    """Check that the window title shows as declared."""
    assert window.windowTitle() == 'Control Point Selection Tool'
