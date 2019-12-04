#!/usr/bin/python

from setuptools import setup, find_packages
from aurademo import _version

long_description = "%s"% (open('README.MD').read())
setup(
    name='aurademo',
    version=_version,
    packages=find_packages(),
    description='turn key setup of demo',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='pinky and the brain',
    author_email='pinky@brain',
    url='',
    python_requires=">=2.7.5",
    classifiers=[
        "License :: Other/Proprietary License",
        "Operating System :: RHEL/CentOS 7",
    ],
    entry_points={
        "console_scripts": [
        'aurademo = aurademo.__main__:__entrypoint__'],
    }
)
