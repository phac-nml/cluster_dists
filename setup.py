#!/usr/bin/env python3
import os
from distutils.core import setup
from setuptools import find_packages
from cluster_dists.version import __version__
author = 'James Robertson'

classifiers = """
Development Status :: 4 - Beta
Environment :: Console
License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)
Intended Audience :: Science/Research
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Bio-Informatics
Programming Language :: Python
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: Implementation :: CPython
Operating System :: POSIX :: Linux
""".strip().split('\n')


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


exec(open('cluster_dists/version.py').read())

setup(
    name='cluster_dists',
    include_package_data=True,
    version=__version__,
    python_requires='>=3.8.2,<4',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    packages=find_packages(exclude=['tests']),
    url='https://github.com/phac-nml/cluster_dists',
    license='GPLv3',
    author='James Robertson',
    author_email='james.robertson@phac-aspc.gc.ca',
    description=(
        'Cluster Dists: Summarizing pairwise distances within categorical groupings'),
    keywords='cgMLST, wgMLST, outbreak, surveillance, clustering, distance matrix',
    classifiers=classifiers,
    package_dir={'cluster_dists': 'cluster_dists'},
    package_data={
        "": ["*.txt"],
    },

    install_requires=[
        'tables==3.8.0',
        'six>=1.16.0',
        'pandas==2.0.2 ',
    ],

    entry_points={
        'console_scripts': [
            'cluster_dists=cluster_dists.main:main',
        ],
    },
)