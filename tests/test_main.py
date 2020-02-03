import os
import sys
from unittest.mock import patch

from click.testing import CliRunner
import matplotlib
matplotlib.use('Agg')  # noqa: E402
import matplotlib.pyplot as plt
import numpy as np
import pytest

import correlateim
import correlateim.cpselect
from correlateim.main import main


@pytest.fixture
def sudoku_image_filenames():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    input_filename_1 = os.path.join(data_dir, 'sudoku.tif')
    input_filename_2 = os.path.join(data_dir, 'sudoku_warped.tif')
    return input_filename_1, input_filename_2


def mock_cpselect(*args, **kwargs):
    # sudoku control points (comparing original to warped sudoku image)
    matched_points_dict = [
        {'point_id': 1,
            'img1_x': 74.269318715307492, 'img1_y': 86.49128717792928,
            'img2_x': 68.287280108254322, 'img2_y': 79.71102703598342},
        {'point_id': 2,
            'img1_x': 489.56025240948878, 'img1_y': 70.388169340807963,
            'img2_x': 438.65899036204462, 'img2_y': 139.03830327800938},
        {'point_id': 3,
            'img1_x': 522.61402060147464, 'img1_y': 520.4279362624618,
            'img2_x': 384.41690922647797, 'img2_y': 541.61624920604243}
    ]
    # FYI: this is the corresponding transformation matrix for these values
    # Transformation matrix
    # [[  0.88153573   0.17703914  -9.68270945]
    #  [ -0.18550115   0.88464383  18.62961837]
    #  [  0.           0.           1.        ]]
    return matched_points_dict


def mock_empty_cpselect(*args, **kwargs):
    # Pretend the user did not select any matched control points
    return []


@pytest.mark.mpl_image_compare
@patch("correlateim.cpselect.cpselect_read_files", new=mock_cpselect)
def test_correlate_images(tmpdir, sudoku_image_filenames):
    input_filename_1, input_filename_2 = sudoku_image_filenames
    filename_out = os.path.join(tmpdir, 'output_correlate_images.png')
    output = correlateim.correlate_images(input_filename_1,
                                          input_filename_2,
                                          filename_out)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.axis('off')
    ax.imshow(output)
    return fig


@patch("correlateim.cpselect.cpselect_read_files", new=mock_empty_cpselect)
def test_empty_correlate_images(tmpdir, sudoku_image_filenames):
    input_filename_1, input_filename_2 = sudoku_image_filenames
    filename_out = os.path.join(tmpdir, 'output_empty.png')
    output = correlateim.correlate_images(input_filename_1,
                                          input_filename_2,
                                          filename_out)
    assert output == None


@patch("correlateim.cpselect.cpselect_read_files", new=mock_cpselect)
def test_main(tmpdir, sudoku_image_filenames):
    input_filename_1, input_filename_2 = sudoku_image_filenames
    filename_out = os.path.join(tmpdir, 'output_correlate_images.png')
    # test click application
    runner = CliRunner()
    result = runner.invoke(main, [input_filename_1, input_filename_2, filename_out])
    expected = (str(mock_cpselect()) +
                "\nTransformation matrix:"
                "\n[[ 0.88153573  0.17703914 -9.68270945]"
                "\n [-0.18550115  0.88464383 18.62961837]"
                "\n [ 0.          0.          1.        ]]"
                "\nSaved image overlay result to: ")
    assert result.exit_code == 0
    assert result.output.startswith(expected)


def test_entry_point():
    exit_value = os.system('correlateim')
    # Expect error since no command line arguments are given.
    # The exact exit value is dependent on the operating system.
    if sys.platform == 'windows':
        # Windows: expect exit value 2 if no command line arguments are given.
        # If the entry point was not correctly configured in setup.py
        # then we would see an exit value of 1 here instead.
        assert exit_value == 2
    elif sys.platform == 'linux':
        # Linux: expect exit value 512 if no command line arguments are given.
        # If the entry point was not correctly configured in setup.py
        # then we would see an exit value of 32512 here instead.
        assert exit_value == 512
    # Would be nice to include Mac exit values here at some point, too.
    else:
        assert False
