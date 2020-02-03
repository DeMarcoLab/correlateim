import matplotlib
matplotlib.use('Agg')  # noqa: E402
import matplotlib.pyplot as plt
import numpy as np
import pytest
import skimage.data

from correlateim import transform


@pytest.fixture(scope="session")
def source_coords():
    src = np.array(
        [[83.09970486, 73.68900001],
         [70.22116071, 490.09526094],
         [518.39449721, 525.29661496],
         [356.9834105, 202.47444154],
         [212.74371599, 351.0069841]])
    return src


@pytest.fixture(scope="session")
def destination_coords():
    dst = np.array(
        [[79.66542642, 69.48044789],
         [137.1895903, 440.38251948],
         [533.84875019, 381.14121638],
         [340.67058791, 128.72175099],
         [241.07651313, 290.99140731]])
    return dst


@pytest.fixture(scope="session")
def example_affine_matrix():
    r = 0.12
    c, s = np.cos(r), np.sin(r)
    matrix_transform = np.array([[c, -s, 0],
                                 [s, c, 50],
                                 [0, 0, 1]])
    return matrix_transform


@pytest.mark.mpl_image_compare
def test_apply_transform(example_affine_matrix):
    image = skimage.data.astronaut()
    output = transform.apply_transform(image, example_affine_matrix)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.axis('off')
    ax.imshow(output)
    return fig


def test_apply_transform_dimension_mismatch(example_affine_matrix):
    image = np.random.random((10, 10, 3))
    with pytest.raises(ValueError):
        transform.apply_transform(image, example_affine_matrix,
                                  multichannel=False)


@pytest.mark.mpl_image_compare
def test_apply_transform_multichannel_false(example_affine_matrix):
    image = skimage.img_as_float(skimage.data.camera())
    output = transform.apply_transform(image, example_affine_matrix,
                                       multichannel=False)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.axis('off')
    ax.imshow(output)
    return fig


@pytest.mark.mpl_image_compare
def test_apply_transform_inverse(example_affine_matrix):
    image = skimage.data.astronaut()
    output = transform.apply_transform(image, example_affine_matrix,
                                       inverse=False)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.axis('off')
    ax.imshow(output)
    return fig


def test_calculate_transform(source_coords, destination_coords):
    output = transform.calculate_transform(source_coords, destination_coords)
    expected_output = np.array(
        [[0.87231142, 0.16466797, -4.19019986],
         [-0.20180383, 0.88444066, 21.69926004],
         [0., 0., 1.]])
    assert np.allclose(output, expected_output)


def test_point_coords(source_coords, destination_coords):
    example_matched_points_dict = [
        {'point_id': 1,
         'img1_x': 73.68900001398778,
         'img1_y': 83.09970485795407,
         'img2_x': 69.48044788854543,
         'img2_y': 79.66542641731121},
        {'point_id': 2,
         'img1_x': 490.0952609419367,
         'img1_y': 70.2211607055433,
         'img2_x': 440.3825194779763,
         'img2_y': 137.18959029807945},
        {'point_id': 3,
         'img1_x': 525.2966149585263,
         'img1_y': 518.3944972094389,
         'img2_x': 381.14121637688663,
         'img2_y': 533.8487501923319},
        {'point_id': 4,
         'img1_x': 202.4744415380957,
         'img1_y': 356.9834104992237,
         'img2_x': 128.7217509896351,
         'img2_y': 340.67058790617},
        {'point_id': 5,
         'img1_x': 351.0069840959002,
         'img1_y': 212.74371599222275,
         'img2_x': 290.991407310011,
         'img2_y': 241.07651312752648}]
    src, dst = transform.point_coords(example_matched_points_dict)
    assert np.allclose(src, source_coords)
    assert np.allclose(dst, destination_coords)
