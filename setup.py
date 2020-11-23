from setuptools import setup

from dynamotable.version import __version__

setup(
    name='dynamotable',
    packages=['dynamotable'],
    version=f'{__version__}',
    license='BSD 3-Clause License',
    description="Read and write table files from the Dynamo software package for subtomogram averaging as pandas dataframes",
    author='Alister Burt',
    author_email='alisterburt@gmail.com',
    url='https://github.com/alisterburt/dynamotable',
    download_url=f'https://github.com/alisterburt/dynamotable/archive/v{__version__}.tar.gz',
    keywords=['IO', 'dynamo', 'table file', 'cryo-EM', 'cryo-ET'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
