import os
import time

import numpy as np
import skimage.color
import skimage.io
import skimage.transform

from correlateim._version import __version__


def imread(filename):
    """Read in a 2D image, and ensure RGB and float type.

    Parameters
    ----------
    filename : str
        Image filename.

    Returns
    -------
    ndarray
        2D image as an RGB numpy array.
    """

    image = skimage.io.imread(filename)

    if image.ndim == 2:
        image = skimage.color.gray2rgb(image)
    image = skimage.img_as_float(image)

    return image


def imsave(filename, image):
    """Save 2D image as 8-bit RGB image.

    Parameters
    ----------
    filename : str
        Output image filename.
    image : ndarray
        2D image as an 8-bit RGB numpy array.

    Returns
    -------
    ndarray
        2D image as an 8-bit RGB numpy array.
    """

    skimage.io.imsave(filename, skimage.img_as_ubyte(image))


def resize_and_save(filename, image, shape):
    """Resize 2D image and save result as 8-bit RGB image.

    Parameters
    ----------
    filename : str
        Output image filename.
    image : ndarray
        2D image as an 8-bit RGB numpy array.
    shape : tuple of ints
        Desired shape for resized image array.

    Returns
    -------
    ndarray
        2D image as an 8-bit RGB numpy array.
    """

    image = skimage.transform.resize(image, shape, anti_aliasing=True)
    skimage.io.imsave(filename, skimage.img_as_ubyte(image))

    return skimage.img_as_ubyte(image)


def _timestamp():
    """Create timestamp string of current local time.

    Returns
    -------
    str
        Timestamp string
    """
    timestamp = time.strftime('%d-%b-%Y_%H-%M%p', time.localtime())
    return timestamp


def save_text(image_filename_1, image_filename_2, output_filename,
              transformation, matched_points_dict):
    """Save text summary of transformation matrix and image control points.

    Parameters
    ----------
    image_filename_1 : str
        Filename of input image 1.
    image_filename_2 : str
        Filename of input image 2.
    output_filename : str
        Filename for saving output overlay image file.
    transformation : ndarray
        Transformation matrix relating the two images.
    matched_points_dict : list of dict
        User selected matched control point pairs.

    Returns
    -------
    str
        Filename of output text file.
    """
    transformation_filename = os.path.splitext(output_filename)[0] + '.npy'
    np.save(transformation_filename, transformation)
    # You can use numpy.load() to read back in .npy numpy files

    output_text_filename = os.path.splitext(output_filename)[0] + '.txt'
    with open(output_text_filename, 'w') as f:
        f.write(_timestamp() + '\n')
        f.write('correlateim version {}\n'.format(__version__))
        f.write('\nUSER INPUT\n')
        f.write(image_filename_1 + '\n')
        f.write(image_filename_2 + '\n')
        f.write('\nTRANSFORMATION MATRIX\n')
        f.write(str(transformation) + '\n')
        f.write('\nUSER SELECTED CONTROL POINTS\n')
        f.write(str(matched_points_dict) + '\n')

    return output_text_filename
