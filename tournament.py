#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM matches")
    cursor.execute("UPDATE players SET num_matches = 0, num_wins = 0")
    connection.commit()
    connection.close()

def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM players")
    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM players")
    connection.commit()
    playerCount = cursor.fetchone()
    return playerCount[0]

def registerPlayer(names):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO players(name, num_wins) VALUES (%s, 0)", (names,))
    connection.commit()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    c = connection.cursor()
    c.execute("SELECT COUNT(id) FROM players")
    total = c.fetchone()[0]

    num_players = countPlayers()
    standings = [None] * num_players

    # every player is present in the standings table
    c.execute("SELECT * FROM wins_view;")
    winners = c.fetchall()
    n = 0
    for player in winners:
		standings[n] = (player[0], player[1], player[2], player[3])
		n += 1
    connection.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    query1 = "INSERT INTO matches(winner, loser) VALUES(%s, %s);"
    cursor.execute(query1, ((winner, ), (loser, ), ))

    query2 = "UPDATE players SET num_wins = num_wins + 1 WHERE id = (%s);"
    cursor.execute(query2, (winner, ))

    query3 = "UPDATE players SET num_matches = num_matches + 1 WHERE id = (%s);"
    cursor.execute(query3, (winner, ))

    query4 = "UPDATE players SET num_matches = num_matches + 1 WHERE id = (%s);"
    cursor.execute(query4, (loser, ))
    connection.commit()
    connection.close()




def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings =playerStandings()
    pairs = [(standings[n-1], standings[n]) for n in range (1, len(standings), 2)]
    swissPairs = [None] * (len(standings) / 2)

    n = 0
    for match in pairs:
      swissPairs[n] = (match[0] [0], match[0] [1], match[1] [0], match[1] [1])
      n += 1
    return swissPairs
