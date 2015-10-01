# Tournament Results #

## Requirements ##
You will need a PostgreSQL server and create a database named 'tournament'

    psql -c 'create database tournament;'

The current user should also have full access to tournament database

## Instructions ##

Here are step by step instructions on how to use tournament_test.py

Clone git repository:

    git clone https://github.com/jasonthomas/udacity.git

Change directory to project2:

    cd udacity/project2

Import tournament database schema:

    psql tournament < tournament.sql


Run tournament_test.py to test tournament.py:

    python tournament_test.py


## Note ##
simulate.py is included for testing purposes only
