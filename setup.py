import setuptools
import os

PACKAGE_NAME = "shelldoc"

short_description = "Google syle shell documentation generator tool"

long_description = short_description
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

about = {}
with open(f"{PACKAGE_NAME}/_version.py", "r") as f:
    exec(f.read(), about)
print(setuptools.find_packages("."))
setuptools.setup(
    name=f"{PACKAGE_NAME}",
    version=about["version_str"],
    author="Antoine Gibek",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antscloud/shelldoc.git",
    project_urls={"Bug Tracker": "https://github.com/antscloud/shelldoc.git",},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": [f"{PACKAGE_NAME}={PACKAGE_NAME}.{PACKAGE_NAME}:main"],},
)
