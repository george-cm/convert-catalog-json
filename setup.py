"""setup.py"""
from setuptools import setup
import convert_catalog_json


package_classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]


setup(
    name="convert_catalog_json",
    version=convert_catalog_json.__version__,
    author="George Murga",
    author_email="george.murga+convert-catalog-json@gmail.com",
    tests_require=["pytest"],
    py_modules=["convert_catalog_json"],
    description="Convert a AEM catalog.json file to csv. Probably not useful for anyone else.",
    license="MIT",
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "convert_catalog_json = convert_catalog_json:main",
        ]
    },
)
