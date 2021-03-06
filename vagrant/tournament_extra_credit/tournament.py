#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament_extra_credit")

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

def deletePlayers():
    """Remove all the player records from the database."""
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("DELETE FROM player;")
    dbconn.commit()
    dbconn.close()

def countPlayers(tournament=None):
    """Returns the number of players currently registered.
    If a tournament id is provided, return the number of players
    entered into that tournament."""
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
    """Returns a list of the players and their win records for the specified
    tournament, sorted by wins.

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
    cursor.execute("""SELECT player_id, name, win_count, match_count 
                      FROM player_standing 
                      WHERE tournament_id = %s;""",
                   (tournament,))
    results = cursor.fetchall()
    dbconn.close()
    return results

def reportMatch(winner, loser, tournament):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament: the id of the tournament in which the match took place
    """
    smaller_id, bigger_id = min(winner, loser), max(winner, loser)
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("INSERT INTO match (player1_id, player2_id, winner_id, tournament_id) VALUES (%s, %s, %s, %s);",
                   (smaller_id, bigger_id, winner, tournament))
    dbconn.commit()
    dbconn.close()

def getMatches(tournament, winner=False):
    """Return a list of matches played in a given tournament, optionally detailing who won."""
    dbconn = connect()
    cursor = dbconn.cursor()
    if winner:
        cursor.execute("SELECT player1_id, player2_id, winner_id FROM match WHERE tournament_id = %s;",
                       (tournament,))
    else:
        cursor.execute("SELECT player1_id, player2_id FROM match WHERE tournament_id = %s;",
                       (tournament,))
    matches = cursor.fetchall()
    dbconn.close()
    return matches

def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match for the given tournament.
  
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
    
    # Get list of matches played
    matches = set(getMatches(tournament))
    
    # Construct swiss pairings
    standings = playerStandings(tournament)    
    
    results = []
    while standings:
        player1 = standings.pop(0)
        id1, name1 = player1[0], player1[1]
        for i in range(len(standings)):
            player2 = standings[i]
            id2, name2 = player2[0], player2[1]
            if set([id1, id2]) not in matches:
                standings.pop(i)
                results.append((id1, name1, id2, name2))
                break
    return results

# Extra functions for extra credit: multiple tournaments

def deleteTournaments():
    """Deletes all tournaments from the database"""
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("DELETE FROM tournament;")
    dbconn.commit()
    dbconn.close()
    
def createTournament(name):
    """Creates a tournament"""
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("INSERT INTO tournament (name) VALUES (%s) RETURNING id", (name,))
    row_id = cursor.fetchone()[0]
    dbconn.commit()
    return row_id
    dbconn.close()

def enterTournament(player_id, tournament_id):
    """Enter a player into a tournament"""
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("INSERT INTO player_tournament (player_id, tournament_id) VALUES (%s, %s);",
                   (player_id, tournament_id))
    dbconn.commit()
    dbconn.close()

