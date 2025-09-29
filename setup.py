""" Package setup. """
import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

requirements = [
    "requests==2.31.0",
    "pandas==1.5.3",
    "tabulate==0.8.7",
    "markdown==3.2.2",
    "numpy==1.26.4",
]

# Development Requirements
requirements_dev = ["pytest==4.*", "black==22.3.0", "pre-commit", "mypy"]

setuptools.setup(
    name="oss-leaderboard",
    version="0.0.1",
    author="lftechnology",
    author_email="opensource@lftechnology.com",
    description="Open Source Leaderboard",
    url="https://github.com/leapfrogtechnology/oss-leaderboard",
    license="MIT",
    packages=setuptools.find_packages(
        where="scripts", exclude=["dist", "build", "*.egg-info"]
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
    ],
    project_urls={
        "Bug Reports": "https://github.com/leapfrogtechnology/oss-leaderboard/issues",
        "Source": "https://github.com/leapfrogtechnology/oss-leaderboard",
    },
)
