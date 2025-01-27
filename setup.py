from setuptools import setup, find_packages

setup(
    name='maskSelector',
    version='1.0.0',
    description='A simple python package to crop image data and create masking arrays for use in Astrophot'
    author='Yashraj Bains',
    author_email='yashrajbains@gmail.com',
    url='https://github.com/yashrajbains/maskSelector',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'astropy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
