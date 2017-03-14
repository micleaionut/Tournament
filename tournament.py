#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import itertools


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
# add query to truncate the table matches
    query = "TRUNCATE matches"
    c.execute(query)
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
# add query to delete all data from players
    query = "DELETE FROM players"
    c.execute(query)
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
# make a count on players and return the number
    query = "SELECT COUNT(*) AS total FROM players"
    c.execute(query)
    total = c.fetchone()
    DB.close()
    return total[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
# insert data into players with name from paramater
    query = "INSERT INTO players (name) VALUES (%s)"
    c.execute(query, (name,))
    DB.commit()
    DB.close()
    return countPlayers()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
# query left join to have tables players and matches
    query = ("SELECT id, name, COUNT(matches.winner) AS wins, "
             "(SELECT games FROM games_view WHERE games_view.id = players.id) "
             "FROM players LEFT JOIN matches "
             "ON players.id = matches.winner "
             "GROUP BY players.id, players.name "
             "ORDER BY wins DESC")
    c.execute(query)
    standings = c.fetchall()
    DB.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
# query to insert data into matches
    query = "INSERT INTO matches (winner, loser) values (%s, %s);"
    c.execute(query, (int(winner), int(loser)))
    DB.commit()
    DB.close()


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
# get standings from playersStandings  make the pairing iterator
    standings = playerStandings()
    pairingsiterator = itertools.izip(*[iter(standings)]*2)
# create a results array
    results = []
    pairings = list(pairingsiterator)
# get pair from pairings and add them to results.
    for pair in pairings:
        id1 = pair[0][0]
        name1 = pair[0][1]
        id2 = pair[1][0]
        name2 = pair[1][1]
        matchup = (id1, name1, id2, name2)
        results.append(matchup)
    return results
