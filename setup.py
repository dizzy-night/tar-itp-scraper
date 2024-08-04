# -*- coding: utf-8 -*-
import setuptools


with open("README.md", encoding="utf-8") as f:
    README_MD = f.read()


setuptools.setup(
    name="tar_itp_scraper",
    version="1.0.0",
    author="DizzyNight",
    author_email="dizzynight2096@gmail.com",
    description="A utility tool to scrape job listings from TARUMT ITP into Python objects",
    long_description=README_MD,
    long_description_content_type="type/markdown",
    license="MIT",
    url="https://github.com/dizzy-night/tar-itp-scraper",
    packages=setuptools.find_packages(exclude=["notebooks"]),
    package_data={'': ['*', '*/*']},
    python_requires='>=3.12'
)
