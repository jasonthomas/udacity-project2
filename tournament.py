#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import itertools
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE table match RESTART IDENTITY")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("TRUNCATE table player RESTART IDENTITY CASCADE")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(id) from player")
    (count,) = c.fetchone()
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    conn = connect()
    c = conn.cursor()
    clean_name = bleach.clean(name)
    c.execute("INSERT INTO player (name) VALUES (%s);", (clean_name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * from standing;")

    standing = c.fetchall()
    conn.close()
    return standing


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO match (winner, loser) VALUES (%s, %s);",
              (winner, loser,))
    conn.commit()
    conn.close()


def getPlayerIds():
    """ Helper function to return all users from the standing view.

    Returns:
        players: a list of player ids
    """

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id from standing")
    players = list(itertools.chain(*c.fetchall()))
    conn.close()
    return players


def potentialCompetitors(id):
    """Returns a list of players that can be potentially matched up with id.
    Args:
      id:  id of player

    Returns:
        players: a list of player ids that can be matched up with id

    """

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT winner, loser from match where winner = %s or "
              "loser = %s", (id, id,))

    result = c.fetchall()
    conn.close()
    previous_competitors = set([i for sub in result for i in sub])
    previous_competitors.add(id)
    players = getPlayerIds()

    # remove previous_competitors from players
    for i in previous_competitors:
        for j in players:
            if j == i:
                players.remove(j)

    return players


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

    # counter
    i = 0

    # empty lists to keep track of assignments
    pairing = []
    player1 = []
    player2 = []

    # get a list of user ids based on the current standing
    players = getPlayerIds()

    conn = connect()
    c = conn.cursor()

    for player in players:
        # check if player has been matched up
        if player not in player1 and player not in player2:
            # get a list of potential players to compete against player
            potentials = potentialCompetitors(player)
            for potential in potentials:
                # check if the potential player is not matched up already
                if potential not in player1 and potential not in player2:
                    # pair up players
                    player1.append(player)
                    player2.append(potential)
                    break

    # iterate through players list and get player names
    while i < len(player1):
        c.execute("SELECT id, name from player where id = %s", (player1[i],))
        result1 = c.fetchone()
        c.execute("SELECT id, name from player where id = %s", (player2[i],))
        result2 = c.fetchone()

        pairing.append(result1 + result2)
        i += 1

    conn.close()
    return pairing
