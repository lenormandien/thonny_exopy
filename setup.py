from setuptools import setup
import os.path
import sys

setupdir = os.path.dirname(__file__)

requirements = []
for line in open(os.path.join(setupdir, "requirements.txt"), encoding="UTF-8"):
    if line.strip() and not line.startswith("#"):
        requirements.append(line)

setup(
    name="thonny-exopy",
    version="1.1.2",
    description="A plug-in which adds exopy NSI IA support for Thonny",
    url="https://github.com/thonny/thonny-exopy/",
    author="prof",
    license="GPL",
    classifiers=[
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: Freeware",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education",
        "Topic :: Software Development",
    ],
    keywords="IDE education programming nsi exopy",
    platforms=["Windows", "macOS", "Linux"],
    python_requires=">=3.7",
    package_data={
        "thonnycontrib.exopy": ["res/*"]
    },
    install_requires=requirements,
    py_modules=["Ed"],
    packages=["thonnycontrib.exopy"],
)
