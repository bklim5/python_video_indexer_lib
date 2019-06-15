import setuptools
from os import path


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='video_indexer',
    version='0.1.6',
    url='https://github.com/bklim5/python_video_indexer_lib',
    description='Common function to query Microsoft Video Indexer',
    author='BK Lim',
    author_email='bklim5@hotmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)