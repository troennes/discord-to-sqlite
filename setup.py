from setuptools import setup
import os

VERSION = "0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="discord-to-sqlite",
    description="Save data from Discord to a SQLite database",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Kim Trønnes",
    url="https://github.com/troennes/discord-to-sqlite",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["discord_to_sqlite"],
    entry_points="""
        [console_scripts]
        discord-to-sqlite=discord_to_sqlite.cli:cli
    """,
    install_requires=["sqlite-utils>=2.8"],
    extras_require={"test": ["pytest"]},
    tests_require=["discord-to-sqlite[test]"],
    classifiers=[
        "Programming Language :: Python :: 3",     
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
)
