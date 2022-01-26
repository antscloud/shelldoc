import setuptools
import os

long_description = "Google syle shell documentation generator tool"
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setuptools.setup(
    name="shelldoc",
    version="0.0.1",
    author="Antoine Gibek",
    description="Google syle shell documentation generator tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antscloud/shelldoc.git",
    project_urls={"Bug Tracker": "https://github.com/antscloud/shelldoc.git",},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    entry_points={"console_scripts": ["shelldoc=shelldoc:main"],},
)
