#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament_extra_credit")

# TO DO: Write test for new functionality
def deleteMatches(tournament=None):
    """If a tournament id is provided, remove all of that tournament's matches from the database.
    Otherwise, remove all the match records from the database."""
    dbconn = connect()
    cursor = dbconn.cursor()
    if tournament:
        cursor.execute("DELETE FROM match WHERE tournament_id = %s;", (tournament,))
    else:
        cursor.execute("DELETE FROM match;")
    dbconn.commit()
    dbconn.close()

# BOOKMARK: Modified up to this point

def deletePlayers():
    """Remove all the player records from the database."""
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("DELETE FROM player;")
    dbconn.commit()
    dbconn.close()

def countPlayers(tournament=None): # TO DO: Add test for added tournament functionality
    """Returns the number of players currently registered."""
    dbconn = connect()
    cursor = dbconn.cursor()
    if tournament:
        cursor.execute("""SELECT num_players
                          FROM players_per_tournament
                          WHERE tournament_id = %s;""",
                      (tournament,))
    else:
        cursor.execute("SELECT COUNT(*) FROM player;")
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
    cursor.execute("INSERT INTO player (name) VALUES (%s) RETURNING id;", (name,))
    row_id = cursor.fetchone()[0]
    dbconn.commit()
    dbconn.close()
    return row_id

def playerStandings(tournament):
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
    cursor.execute("SELECT player_id, name, win_count, match_count FROM player_standing WHERE tournament_id = %s;",
                   (tournament,))
    results = cursor.fetchall()
    dbconn.close()
    return results

def reportMatch(winner, loser): # TO DO: Add tournament parameter.
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    smaller_id, bigger_id = min(winner, loser), max(winner, loser)
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("INSERT INTO match (player1_id, player2_id, winner_id) VALUES (%s, %s, %s);",
                   (smaller_id, bigger_id, winner))
    dbconn.commit()
    dbconn.close()
 
def swissPairings(): # TO DO: Add match parameter
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
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("SELECT id1, name1, id2, name2 FROM swiss_pairing;")
    results = cursor.fetchall()
    dbconn.close()
    return results

# Extra functions for extra credit: multiple tournaments

def deleteTournaments():
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("DELETE FROM tournament;")
    dbconn.commit()
    dbconn.close()
    
def createTournament(name):
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("INSERT INTO tournament (name) VALUES (%s) RETURNING id", (name,))
    row_id = cursor.fetchone()[0]
    dbconn.commit()
    return row_id
    dbconn.close()

def enterTournament(player_id, tournament_id): # TO DO: New function. Write test
    """Enter a player into a tournament"""
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("INSERT INTO player_tournament (player_id, tournament_id) VALUES (%s, %s);",
                   (player_id, tournament_id))
    dbconn.commit()
    dbconn.close()

