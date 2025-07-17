#!/usr/bin/env python3
"""
Setup script for Bat Broom - Windows Temporary Files Cleanup GUI
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from the main module
def get_version():
    """Extract version from the main module"""
    version = "1.0.0"
    return version

setup(
    name="bat-broom",
    version=get_version(),
    author="Bat Broom Contributors",
    author_email="",
    description="A user-friendly Python GUI application for safely cleaning Windows temporary files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eb1mo/bat-broom",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "Environment :: Win32 (MS Windows)",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "dev": [
            "pyinstaller>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bat-broom=bat_broom:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="windows, cleanup, temporary files, gui, tkinter, system maintenance",
    project_urls={
        "Bug Reports": "https://github.com/eb1mo/bat-broom/issues",
        "Source": "https://github.com/eb1mo/bat-broom",
        "Documentation": "https://github.com/eb1mo/bat-broom#readme",
    },
) 