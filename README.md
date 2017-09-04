# Swiss Tournament

A smarter tournament system in which players are paired with those of similar skill level and everyone competes in every round. More fair than an elimination bracket and more efficient than a round-robin tournament.

A PostgreSQL database stores match results, and a Python module queries the database to rank and pair players. When two players have the same win record, ties are broken by summing the win record of each player's previous opponents.

## Requirements

Python >2.7 and <3.0.

psycopg2

PostgreSQL

Set up

To create the tournament database and tables:

>>> psql initialize the interactive terminal for PostgreSQL

>>> \i tournament.sql execute the contents of tournament.sql to create database, tables, and views

>>> \q exit Psql interactive

Usage

Start the Python interpreter and import the tournament.py module.

## tournament.sql

This file is used to set up the database used to store the players in the 
tournament as well as the matches each of which occupy their own table.

Players associate themselves with a unique id, their name, the number of wins &
losses they have, and the total number of games they have played all recorded in
the Players table.

The matches table contains a unique id and the winner & loser of the match.


A view is also created which "highlights" specific columns from the Players
table, namely the wins in descending order.

 
## tournament.py
This file contains all the methods necessary to get a tournament up and running,
gather information about the state of the tournament & players, as well as clear
the tournament data. It also finds the specific matches necessary to create a 
swiss-style tournament.

Methods defined in this file are listed below:
connect()
deleteMatches()
deletePlayers()
countPlayers()
registerPlayer(name)
playerStandings()
reportMatch(winner, loser)
swissPairings()

Further detail about the arguments and return values of above methods can be 
found in tournament.py.


## tournament_test.py
This file is a test script used to check the functionality of the swiss-style 
tournament. It clears the tables in the database, populates it with players and 
games, and is used to simulate a simple tournament.

Specifically, it runs the following self-explanatory methods:

    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
