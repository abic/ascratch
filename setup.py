from setuptools import setup, find_packages
from os import path

# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ascratch",
    version="0.1.0",
    description="A Scratch project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abic/ascratch",
    author="Jeffrey T. Peckham",
    author_email="abic@ophymx.com",
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="sample setuptools development",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    python_requires=">=3.8",
    install_requires=[
        "cython",
        "uvloop",
        "aiohttp",
        "aiosqlite",
        "dependency-injector",
        "toml",
        "click",
    ],
    extras_require={"dev": []},
    dependency_links=[],
    project_urls={},
)
