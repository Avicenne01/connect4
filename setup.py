import setuptools
from pathlib import Path

SRC_DIR = "src"

REQUIREMENTS_FILE = Path("requirements.txt")


def get_install_requires():
    with REQUIREMENTS_FILE.open() as file:
        return [package.strip() for package in file.readlines()]


package_name = Path.cwd().name
python_version = "3.8.5"
install_requires = get_install_requires()

setuptools.setup(
    name=package_name,
    version="dev",
    author="Merchrist KIKI",
    author_email="dona.merchrist@gmail.com",
    packages=setuptools.find_packages(where=SRC_DIR),
    package_dir={"": SRC_DIR},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=f">={python_version}",
    install_requires=install_requires,
)
