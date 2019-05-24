import os

import numpy as np
import pytest

import correlateim.io


def test_imread_rgb():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.realpath(os.path.join(
        current_directory, '..', 'data', 'sudoku.tif'))
    output = correlateim.io.imread(filename)
    assert output.dtype == float
    assert output.shape == (563, 558, 3)


def test_imread_grayscale():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.realpath(
        os.path.join(current_directory, '..', 'data',
                     'worm_scanning-electron-microscopy.tif'))
    output = correlateim.io.imread(filename)
    assert output.dtype == float
    assert output.shape == (2048, 3072, 3)


def test_imsave(tmpdir):
    ourput_directory = tmpdir.mkdir("subdir")
    output_filename = os.path.join(ourput_directory, 'output.png')
    image = np.random.random((256, 256, 3))
    correlateim.io.imsave(output_filename, image)


@pytest.mark.parametrize("original_shape, expected_shape",
                         [((200, 200), (457, 532)),
                          ((200, 200), (144, 139)),
                             ((200, 200, 3), (457, 532, 3)),
                             ((200, 200, 3), (457, 532, 1)),
                          ])
def test_resize_and_save(original_shape, expected_shape, tmpdir):
    image = np.random.random(original_shape)
    ourput_directory = tmpdir.mkdir("subdir")
    filename = os.path.join(ourput_directory, 'output.png')
    output = correlateim.io.resize_and_save(filename, image, expected_shape)
    assert output.shape == expected_shape


def test_save_text(tmpdir):
    output_iamge_filename = os.path.abspath(os.path.join(tmpdir, 'output.png'))
    expected_text_filename = os.path.abspath(
        os.path.join(tmpdir, 'output.txt'))
    transformation = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    matched_points_dict = [{'key1': 1, 'key2': 2, 'key3': 3}]
    result = correlateim.io.save_text('input_filename_1.tif',
                                      'input_filename_2.tif',
                                      output_iamge_filename,
                                      transformation,
                                      matched_points_dict)
    assert result == expected_text_filename
