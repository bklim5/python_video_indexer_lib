import setuptools


setuptools.setup(
    name='video_indexer',
    version='0.1.3',
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
    ]
)