#!/usr/bin/env python

from setuptools import setup, find_packages


with open('VERSION', 'r') as version_file:
    VERSION = version_file.read()


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='graphbrain-server',
    version=VERSION,
    author='Telmo Menezes et al.',
    author_email='telmo@telmomenezes.net',
    description='Graphbrain server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://graphbrain.net',
    license='MIT',
    keywords=['NLP', 'AI', 'Knowledge Representation', 'Knowledge Systems',
              'Natural Language Understanding', 'Text Analysis', 'Cognition'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Sociology'
    ],
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=[
        'graphbrain',
        'flask',
        'flask-cors'
    ],
    include_package_data=True,
    entry_points='''
        [console_scripts]
        gbserver=gbserver.__main__:cli
    '''
)
