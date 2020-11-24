import click
import os
import sqlite_utils
import json
import zipfile
from discord_to_sqlite import utils

@click.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument(
    "zip_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
def cli(db_path, zip_path):
    """Import data from your Discord Data Package into a SQLite database.
    """
    db = sqlite_utils.Database(db_path)
    zf = zipfile.ZipFile(zip_path)
    utils.save_all(db, zf)