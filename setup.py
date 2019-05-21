from setuptools import setup, find_packages

from correlateim._version import __version__

descr = """2D image correlation using matched points."""

DISTNAME = 'correlateim'
DESCRIPTION = '2D image correlation using matched points.'
LONG_DESCRIPTION = descr
MAINTAINER = 'Genevieve Buckley'
URL = 'https://github.com/DeMarcoLab/correlateim'
DOWNLOAD_URL = 'https://github.com/DeMarcoLab/correlateim'
VERSION = __version__
PYTHON_VERSION = (3, 5)
INST_DEPENDENCIES = [
    'matplotlib',
    'numpy',
    'Pillow',
    'pyqt5',
    'scikit-image',
    'scipy',
]

if __name__ == '__main__':
    setup(name=DISTNAME,
          version=__version__,
          url=URL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          author=MAINTAINER,
          packages=find_packages(),
          install_requires=INST_DEPENDENCIES
          )
