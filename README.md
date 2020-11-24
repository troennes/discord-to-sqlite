# discord-to-sqlite

Import data from your Discord Data Package into a SQLite database.

## How to install

    $ pip install discord-to-sqlite

First, request [your Discord data]( https://support.discord.com/hc/en-us/articles/360004027692-Requesting-a-Copy-of-your-Data) - wait for the email and download the zip file.

This tool currently supports importing messages, friends, servers and channels. More may be added in the future.

## How to use

Import the downloaded `package.zip` file with the following command:

    $ discord-to-sqlite discord.db path/to/package.zip

This will create a database file called `discord.db` if one does not already exist. 

## Browsing your data with Datasette

Once you have imported Discord data into a SQLite database file you can browse your data using [Datasette](https://github.com/simonw/datasette). Install Datasette like so:

    $ pip install datasette

Now browse your data by running this and then visiting `http://localhost:8001/`

    $ datasette discord.db

## Credits

This package is heavily inspired by [google-takeout-to-sqlite](https://github.com/dogsheep/google-takeout-to-sqlite) by [Simon Willison](https://simonwillison.net/2019/Oct/7/dogsheep/).

The package is designed to fit into the [dogsheep](https://dogsheep.github.io/)/[datasette](https://github.com/simonw/datasette) ecosystems.
