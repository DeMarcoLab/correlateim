import numpy as np
import pytest

from correlateim import cpselect


@pytest.fixture
def window(qtbot):
    """Pass the application to the test functions via a pytest fixture."""
    image_1 = np.random.random((500, 500))
    image_2 = np.random.random((500, 500))
    app, window = cpselect.create_window(image_1, image_2)
    qtbot.add_widget(window)
    return window


def test_window_title(window):
    """Check that the window title shows as declared."""
    assert window.windowTitle().startswith('Control Point Selection Tool')
