import setuptools

setuptools.setup(
    name='image-to-palette',
    version='1.1.1',
    author="Urij Horuzij",
     description="This is a test package.",
     url="https://github.com/UrijHoruzij/image-to-palette",
    install_requires=[
        "argparse",
        "Pillow",
        "matplotlib",
        "scikit-learn",
        "numpy"
    ]
)