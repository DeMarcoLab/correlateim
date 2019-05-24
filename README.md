# correlateim

`correlateim` is a package for aligning images.

The user interactively selects matching point pairs, then the transformation matrix is calculated and an image overlay result is returned.

The interactive GUI module is adapted from [cpselect](https://github.com/adal02/cpselect), a Python port of the MATLAB cpselect functionality.

## Quickstart

### Installation

See the `correlateim` [releases page](https://github.com/DeMarcoLab/correlateim/releases). Downloading a precompiled `.exe` file is the simplest and quickest method.

### Demo data

Demonstration data can be found in the [data/](data/) directory.

### Running the program

`correlateim` is supported on Python 3.6
It accepts 8-bit grayscale or RGB images as input.

To run the `correlateim.exe` executable file downloaded from the [releases page](https://github.com/DeMarcoLab/correlateim/releases), launch it from the command line:

```
path/to/correlateim.exe path/to/input_image_1.tif path/to/input_image_2.tif path/for/output_file.tif
```

It will take a few seconds to launch, then you will see the interactive point selection window appear.

You'll see this user interface:

![User selects matched control points](examples/example_point_selection.png)

Clicking the "Pick Mode" button at the bottom right will allow you to select matched control point pairs. You can add or remove point pairs, see the GUI help dialogs for more detail.

When you are satisfied, click the 'Return' button in the bottom right hand corner. This will close the interactive window, calculate the transformation and display the overlaid images.

![Result as an image overlay](examples/example_output.png)


### Alternative installation methods
There are a number of alternative installation options available:

* download the pre-compiled executable files
* download the python wheel (can be installed by: `pip install filename.whl`)
* Install from the `correlateim` master branch using pip:
    ```
    pip install git+https://github.com/DeMarcoLab/correlateim.git
    ```
* clone the repository and install the development version, as described in the next section.


### For developers
`correlateim` is supported on Python 3.6

#### Development installation

Fork the reporitory on GitHub.

Clone your new forked repository:
```
git clone https://github.com/YOUR_GITHUB_USERNAME/correlateim.git
cd correlateim
```

Create a new virtual environment for your development work.
[Conda](https://docs.conda.io/en/latest/) is highly recommended.
```
conda env create -f environment.yml
conda activate correlateim
```

Install the requirements into your development environment.
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Finally, install `correlateim` as an editable installation.
```
pip install -e .
```

Alternatively, you can complete this last step with:
```
python setup.py develop
```

#### Running the development version

From the command line:
```
python correlateim/main.py path/to/input_image_1.tif path/to/input_image_2.tif path/for/output_file.tif
```

From within python:
```
$ python
>>> import correlateim
>>> correlateim.correlate_images('path/to/input_image_1.tif', 'path/to/input_image_2.tif', 'path/for/output_file.tif')
```

### Running the tests
[Pytest](https://pytest.readthedocs.io/en/latest/) is used as the testing framework for this project.

To run the test suite from the root directory of the repository:
```
py.test
```


#### Generating new baseline images for pytest matplotlib plugin

The `pytest-mpl` plugin is used to test image results against baseline versions. If you need to generate new baseline images, run:
```
py.test --mpl-generate-path=tests\baseline
```

This will overwrite the current files in `tests\baseline\`, so if you are unsure you may like to specify a different path and copy the files to the baseline directory afterwards.

### Packaging
#### Executables with Pyinstaller
Pyinstaller is used to create binaries: https://www.pyinstaller.org/

To run pyinstaller:
```
pyinstaller correlateim/main.py
```

This will generate output files in the `dist/` directory.

#### Python wheels

To bulid the python wheel, run:
```
python setup.py bdist_wheel
```

This will geerate a `.whl` file in the `dist/` directory.

### Reporting issues

Technical issues can be logged at https://github.com/DeMarcoLab/correlateim/issues
