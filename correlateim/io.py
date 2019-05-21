import skimage.color
import skimage.io
import skimage.transform


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
