import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="domo_python",
    version="0.0.10",
    author="Big Squid, Inc.",
    author_email="bcooper@bigsquid.com",
    description="Domo API functions to import and export data into usable Pandas dataframes and manage your Domo instancea",
    url="https://github.com/brockcooper/domo_python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
)