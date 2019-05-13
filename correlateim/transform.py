import numpy as np
import scipy.ndimage as ndi
from skimage.transform import AffineTransform


def apply_transform(image, transformation, inverse=True, multichannel=True):
    """Apply transformation to a 2D image.

    Parameters
    ----------
    image : ndarray
        Input image array. 2D grayscale image expected, or
        2D plus color channels if multichannel kwarg is set to True.
    transformation : ndarray
        Affine transformation matrix. 3 x 3 shape.
    inverse : bool, optional
        Inverse transformation, eg: aligning source image coords to destination
        By default `inverse=True`.
    multichannel : bool, optional
        Treat the last dimension as color, transform each color separately.
        By default `multichannel=True`.

    Returns
    -------
    ndarray
        Image warped by transformation matrix.
    """

    if inverse:
        transformation = np.linalg.inv(transformation)

    if not multichannel:
        if image.ndim != transformation.shape[0] - 1:
            raise ValueError('Unexpected number of image dimensions for the '
                             'input transformation. Did you need to use: '
                             'multichannel=True ?')
        image = np.expand_dims(image, -1)

    # move channel axis to the front for easier iteration over array
    image = np.moveaxis(image, -1, 0)
    warped_img = np.array([ndi.affine_transform((img_channel), transformation)
                           for img_channel in image])
    warped_img = np.moveaxis(warped_img, 0, -1)

    return warped_img


def calculate_transform(src, dst, model=AffineTransform()):
    """Calculate transformation matrix from matched coordinate pairs.

    Parameters
    ----------
    src : ndarray
        Matched row, column coordinates from source image.
    dst : ndarray
        Matched row, column coordinates from destination image.
    model : scikit-image transformation class, optional.
        By default, model=AffineTransform()


    Returns
    -------
    ndarray
        Transformation matrix.
    """

    model.estimate(src, dst)
    print('Transformation matrix:')
    print(model.params)

    return model.params


def point_coords(matched_points_dict):
    """Create source & destination coordinate numpy arrays from cpselect dict.

    Matched points is an array where:
    * the number of rows is equal to the number of points selected.
    * the first column is the point index label.
    * the second and third columns are the source x, y coordinates.
    * the last two columns are the destination x, y coordinates.

    Parameters
    ----------
    matched_points_dict : dict
        Dictionary returned from cpselect containing matched point coordinates.

    Returns
    -------
    (src, dst)
        Row, column coordaintes of source and destination matched points.
        Tuple contains two N x 2 ndarrays, where N is the number of points.
    """

    matched_points = np.array([list(point.values())
                               for point in matched_points_dict])
    src = np.flip(matched_points[:, 1:3], axis=1)  # flip for row, column index
    dst = np.flip(matched_points[:, 3:], axis=1)   # flip for row, column index

    return src, dst
