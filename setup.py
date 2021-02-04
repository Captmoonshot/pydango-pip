import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()


setup(
	name="pydango-pip",
    version="1.0.0",
    description="Pip installable database schema that attempts to mimic the Fandango database",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Captmoonshot/pydango-pip",
    author="Sammy Lee",
    author_email="sam@gygantor.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pydango"],
    include_package_data=True,
    install_requires=[
            "sqlalchemy==1.3.22",
            "sqlalchemy-utils==0.36.6", 
            "psycopg2-binary==2.8.6",
            "passlib==1.7.4",
            "python-dateutil==2.8.1",    
        ],
    entry_points={
        "console_scripts": [
            "pydango=pydango.__main__:main",
        ]
    },
)



