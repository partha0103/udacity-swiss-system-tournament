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
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("DELETE FROM matches;")
    dbconn.commit()
    dbconn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("DELETE FROM players;")
    dbconn.commit()
    dbconn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("SELECT COUNT(*) FROM players;")
    count = cursor.fetchall()[0][0]
    dbconn.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    dbconn.commit()
    dbconn.close()

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
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("SELECT player_id, name, win_count, match_count FROM player_standings;")
    results = cursor.fetchall()
    dbconn.close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    smaller_id, bigger_id = min(winner, loser), max(winner, loser)
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("INSERT INTO matches (player1_id, player2_id, winner_id) VALUES (%s, %s, %s);",
                   (smaller_id, bigger_id, winner))
    dbconn.commit()
    dbconn.close()
 
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
    standings = [(player[0], player[1]) for player in playerStandings()]
    # put standings into a list of pairs like ((id1, name2), (id2, name2)) 
    pairings = zip(standings[::2], standings[1::2]) # http://stackoverflow.com/q/4628290
    # flatten pairs of standings e.g. ((id, name), (id2, name2)) becomes (id, name, id2, name2)
    pairings = [(x[0][0], x[0][1], x[1][0], x[1][1]) for x in pairings]
    return pairings

