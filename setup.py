from setuptools import setup, find_packages

from correlateim._version import __version__

DISTNAME = 'correlateim'
MAINTAINER = 'Genevieve Buckley'
URL = 'https://github.com/DeMarcoLab/correlateim'
DOWNLOAD_URL = 'https://github.com/DeMarcoLab/correlateim'
VERSION = __version__
PYTHON_VERSION = (3, 5)
DESCRIPTION = '2D image correlation using matched points.'

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()


def parse_requirements_file(filename):
    with open(filename) as fid:
        requires = [l.strip() for l in fid.readlines() if l]

    return requires


INSTALL_REQUIRES = parse_requirements_file('requirements.txt')

if __name__ == '__main__':
    setup(name=DISTNAME,
          version=__version__,
          url=URL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          author=MAINTAINER,
          packages=find_packages(),
          install_requires=INSTALL_REQUIRES,
          entry_points={
              'console_scripts': [
                'correlateim = correlateim.main:main',
                'correlateim-from-file = correlateim.main:main_from_file'
                ],
              },
          )
