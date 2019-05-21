import numpy as np
import skimage


def max_intensity_projection(image, start_slice=0, end_slice=None):
    """
    Returns maximum intensity projection of fluorescence image volume.

    Parameters
    ----------
    image : expecting numpy.ndarray with dimensions (pln, row, col, ch)
    start_slice : expecting integer.  First image index of z sub-stack
    end_slice : expecting integer.  Last image index of z sub-stack, not incl.

    Returns
    -------
    projected_max_intensity

    """

    # Check input validity
    if image.ndim != 4:
        raise ValueError("expecting numpy.ndarray with dimensions "
                         "(pln, row, col, ch)")

    # Allow optional selection of sub-region of full image stack
    if end_slice is None:
        image = image[start_slice:, ...]
    else:
        image = image[start_slice:end_slice, ...]

    # move channel axis to the front for easier iteration over array
    image = np.moveaxis(image, -1, 0)
    results = []
    for channel_image in image:
        max_intensity = np.max(channel_image, axis=0)
        results.append(max_intensity)
    projected_max_intensity = np.stack(results, axis=-1)

    return projected_max_intensity


def overlay_images(image_1, image_2, transparency=0.5):
    """Blend two RGB images together.

    Parameters
    ----------
    image_1 : ndarray
        2D RGB image.
    image_2 : ndarray
        2D RGB image.
    transparency : float, optional
        Transparency alpha parameter between 0 - 1, by default 0.5

    Returns
    -------
    ndarray
        Blended 2D RGB image.
    """

    image_1 = skimage.img_as_float(image_1)
    image_2 = skimage.img_as_float(image_2)
    blended = transparency * image_1 + (1 - transparency) * image_2
    blended = np.clip(blended, 0, 1)

    return blended
