# Flask Login Template

This package contains all of the necessary components to run a website with
user authentication on Flask and Bootstrap.

The necessary database schema can be found in the docs directory (MySQL).


## Installation

These installation notes are still in progress...

To setup your database, run this command:

    mysql < docs/schema.sql

## Roadmap

The following items are planned for a future release:
 - Forgot Password link powered by SendGrid
 - About page explaining how things work
 - Install instructions in README
 - Add optional sample data with setup
 - Fill out README with full explanations about how things work, and what powers what
 - Separate out sqlalchemy models into separate file
 - Define database name in install file or setup file
 - Make it easier to build an app on top of this, and be able to update this separately to add new functionality
 - Fail nicely with formatted error message if app can't connect to database
 - Offer a weaker password hash algorithm than blowfish (py-bycrypt) that is pure python for things like Google App Engine

## Roadmap Progress
 - Add default profile page - v0.0.4 (April 16, 2014)
 - Password hash and salt - v0.0.3 (April 15, 2014)
 - Remember me - v0.0.2 (April 8, 2014)
