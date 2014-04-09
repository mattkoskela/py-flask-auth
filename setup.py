import os
from setuptools import setup

LONG_DESC = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

with open("okr/version.py") as f:
    exec(f.read())

setup(
    name="py-flask-auth",
    version=__version__,
    author="Matt Koskela",
    author_email="mattkoskela@gmail.com",
    packages=["example"],
    url="https://github.com/mattkoskela/py-flask-auth",
    include_package_data=True,
    zip_safe=False,
    license="LICENSE.txt",
    description="This package contains all of the necessary components to run a website with user authentication on Flask and Bootstrap.",
    long_description=LONG_DESC,
    install_requires=[
        "flask==0.10.1",
        "flask-login==0.2.10",
        "flask-sqlalchemy==1.0",
        "PyMySQL==0.6.1",
        "sqlalchemy==0.9.4",
    ]
)
