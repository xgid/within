"""
Install the within package.
"""
from distultils.core import setup


setup(
    name="within",
    version="0.1.0",
    author="Brendan Curran-Johnson",
    author_email="brendan@bcjbcj.ca",
    packages=['within'],
    url="https://github.com/bcj/within",
    license="LICENSE.txt",
    description="A collection of context managers.",
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
