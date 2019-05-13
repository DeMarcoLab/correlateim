import os

import click
from cpselect.cpselect import cpselect
import matplotlib.pyplot as plt

from correlateim import io
from correlateim import imageproc
from correlateim import transform


@click.command()
@click.argument('input_filename_1')
@click.argument('input_filename_2')
@click.argument('output_filename')
def main(input_filename_1, input_filename_2, output_filename):
    image_1 = io.imread(input_filename_1)
    image_2 = io.imread(input_filename_2)
    temp_filename = os.path.join(os.path.split(output_filename)[0],
                                               'temp_image1.tif')
    image_1 = io.resize_and_save(temp_filename, image_1, image_2.shape)
    # User select matched control points
    matched_points_dict = cpselect(temp_filename, input_filename_2)
    print(matched_points_dict)
    # Calculate and apply affine transformation
    src, dst = transform.point_coords(matched_points_dict)
    transformation = transform.calculate_transform(src, dst)
    image_1_aligned = transform.apply_transform(image_1, transformation)
    result = imageproc.overlay_images(image_1_aligned, image_2)
    # Finish and tidy up
    os.remove(temp_filename)
    io.imsave(output_filename, result)
    plt.imshow(result)
    plt.show()
    return result


if __name__=='__main__':
    main()
