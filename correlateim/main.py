import os

import click
import matplotlib.pyplot as plt
import skimage.color
import skimage.transform

from correlateim import imageproc
from correlateim import transform
from correlateim.cpselect import cpselect_read_files
from correlateim.io import save_text


@click.command()
@click.argument('input_filename_1')
@click.argument('input_filename_2')
@click.argument('output_filename')
def main(input_filename_1, input_filename_2, output_filename):
    result = correlate_images(input_filename_1, input_filename_2, output_filename)
    return result


def correlate_images(input_filename_1, input_filename_2, output_filename):
    # User select matched control points
    matched_points_dict = cpselect_read_files(input_filename_1,
                                              input_filename_2)
    if matched_points_dict == []:
        print('No control points selected, exiting.')
        return
    print(matched_points_dict)
    # Calculate and apply affine transformation
    src, dst = transform.point_coords(matched_points_dict)
    transformation = transform.calculate_transform(src, dst)
    # Align images
    image_1 = skimage.color.gray2rgb(plt.imread(input_filename_1))
    image_2 = skimage.color.gray2rgb(plt.imread(input_filename_2))
    image_1 = skimage.transform.resize(image_1, image_2.shape,
                                       anti_aliasing=True)
    image_1_aligned = transform.apply_transform(image_1, transformation)
    result = imageproc.overlay_images(image_1_aligned, image_2)
    # Finish and tidy up
    save_text(input_filename_1, input_filename_2, output_filename,
              transformation, matched_points_dict)  # saves text summary
    plt.imsave(output_filename, result)
    print('Saved image overlay result to: '
          '{}'.format(os.path.abspath(output_filename)))
    plt.imshow(result)
    plt.show()
    return result


if __name__ == '__main__':
    main()
