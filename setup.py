from setuptools import setup, find_packages
import pkg_resources
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name = 'prog_algs',
    version = '1.1.0',
    description = "The NASA Prognostics Algorithm Package is a framework for model-based prognostics (computation of remaining useful life) of engineering systems. It includes algorithms for state estimation and prediction, including uncertainty propagation. The algorithms use prognostic models (see prog_models) to perform estimation and prediction. The package enables rapid development of prognostics solutions for given models of components and systems. Algorithms can be swapped for comparative studies and evaluations",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/nasa/prog_algs',
    author = 'Christopher Teubert',
    author_email = 'christopher.a.teubert@nasa.gov',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing', 
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: Other/Proprietary License ',   
        'Programming Language :: Python :: 3',     
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords = ['prognostics', 'diagnostics', 'fault detection', 'fdir', 'prognostics and health management', 'PHM', 'health management'],
    package_dir = {"":"src"},
    packages = find_packages(where = 'src'),
    python_requires='>=3.6, <3.10',
    install_requires = [
        'numpy',
        'scipy',
        'filterpy',
        'matplotlib',
        'prog_models'
    ],
    license = 'NOSA',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/nasa/prog_algs/issues',
        'Organization': 'https://prognostics.nasa.gov/',
        'Source': 'https://github.com/nasa/prog_algs',
    }
)