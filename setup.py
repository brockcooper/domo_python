import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="domo_python",
    version="0.0.1",
    author="Big Squid, Inc.",
    author_email="bcooper@bigsquid.com",
    description="Domo API functions to import and export data into usable Pandas dataframes and manage your Domo instancea",
    url="https://github.com/brockcooper/domo_python",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)