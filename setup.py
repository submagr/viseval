import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="viseval",
    version="0.0.2.2",
    author="Shubham Agrawal",
    author_email="agshubh191@gmail.com",
    description="Visualization tool for your evaluation folder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/submagr/viseval",
    packages=setuptools.find_packages(),
    install_requires=["dominate"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
