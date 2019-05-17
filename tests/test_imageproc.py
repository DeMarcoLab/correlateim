import numpy as np
import pytest
from correlateim.imageproc import (max_intensity_projection,
                                   overlay_images)


def test_max_intensity_projection():
    input_image = [[[0, 1, 4], [2, 1, 1], [0, 2, 0]],
                   [[4, 1, 0], [1, 1, 2], [2, 0, 2]]]
    input_image = np.expand_dims(input_image, -1)
    output_image = max_intensity_projection(input_image)
    # took out leading main^
    expected = [[4, 1, 4], [2, 1, 2], [2, 2, 2]]
    expected = np.expand_dims(expected, -1)
    assert np.allclose(output_image, expected)


def test_mip_slicing():
    input_image = [[[0, 1, 4], [2, 1, 1], [0, 2, 0]],
                   [[4, 1, 0], [1, 1, 2], [2, 0, 2]]]
    input_image = np.expand_dims(input_image, -1)
    output_image = max_intensity_projection(input_image, start_slice=0,
                                            end_slice=1)
    # took out leading main^
    expected = [[[0, 1, 4], [2, 1, 1], [0, 2, 0]]]
    expected = np.expand_dims(expected, -1)
    assert np.allclose(output_image, expected)


def test_mip_dimensions():
    input_image = [[[0, 1, 4], [2, 1, 1], [0, 2, 0]],
                   [[4, 1, 0], [1, 1, 2], [2, 0, 2]]]
    input_image = np.array(input_image)

    with pytest.raises(ValueError):
        max_intensity_projection(input_image)
    # took out leading main^


def test_mip_channels():
    input_image = [[[[0, 2, 7], [1, 3, 1], [4, 1, 7]],
                    [[2, 7, 1], [1, 1, 6], [1, 0, 8]],
                    [[0, 1, 2], [2, 1, 2], [0, 0, 5]]],
                   [[[4, 8, 9], [1, 2, 4], [0, 0, 2]],
                    [[1, 3, 3], [1, 1, 9], [2, 4, 8]],
                    [[2, 1, 1], [0, 5, 2], [2, 1, 9]]]]
    input_image = np.array(input_image)
    output_image = max_intensity_projection(input_image)
    expected = [[[4, 8, 9], [1, 3, 4], [4, 1, 7]],
                [[2, 7, 3], [1, 1, 9], [2, 4, 8]],
                [[2, 1, 2], [2, 5, 2], [2, 1, 9]]]
    assert np.allclose(output_image, expected)


def test_overlay_images_int():
    shape = (2, 2, 3)
    image_1 = (np.ones(shape) * 100).astype(np.uint8)
    image_2 = (np.ones(shape) * 200).astype(np.uint8)
    blended_value = 150 / 255  # divide by 255 since output is float not 8-bit
    expected = (np.ones(shape) * blended_value)
    output_image = overlay_images(image_1, image_2, transparency=0.5)
    assert np.allclose(output_image, expected)


def test_overlay_images_float():
    shape = (2, 2, 3)
    image_1 = np.ones(shape) * 0.3
    image_2 = np.ones(shape) * 0.7
    blended_value = 0.5  # mid-point value between 0.3 and 0.7
    expected = (np.ones(shape) * blended_value)
    output_image = overlay_images(image_1, image_2, transparency=0.5)
    assert np.allclose(output_image, expected)
