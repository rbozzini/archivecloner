import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="archivecloner",
    version="0.0.1",
    author="Rossella Bozzini",
    author_email="rossellabozzini@gmail.com",
    description="Archive cloner for photos and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rbozzini/archivecloner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)