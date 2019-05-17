#

## Quickstart
install from release binary
see the video/gif

## Installation

```
pip install git+https://github.com/DeMarcoLab/correlateim.git
```

## Running the program
### Demo data


## For developers
### Development installation
```
git clone https://github.com/DeMarcoLab/correlateim.git
cd correlateim
```

```
conda env create -f environment.yml
conda activate correlateim
```

```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

```
pip install -e .
```

### Running the tests

```
py.test
```

#### Generating new baseline images for pytest matplotlib plugin

```
py.test --mpl-generate-path=tests\baseline
```

### Packaging
Pyinstaller is used to create binaries: https://www.pyinstaller.org/

```
pyinstaller correlateim/main.py
```