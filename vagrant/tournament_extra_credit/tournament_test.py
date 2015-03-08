#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    # Modified to work with a database with multiple tournaments
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    p1 = registerPlayer("Melpomene Murray")
    p2 = registerPlayer("Randy Schwartz")
    t1 = createTournament("t1")
    enterTournament(p1, t1)
    enterTournament(p2, t1)
    standings = playerStandings(t1)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    # Modified to work with a database with multiple tournaments
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    t1 = createTournament("t1")
    p1 = registerPlayer("Bruno Walton")
    p2 = registerPlayer("Boots O'Neal")
    p3 = registerPlayer("Cathy Burton")
    p4 = registerPlayer("Diane Grant")
    enterTournament(p1, t1)
    enterTournament(p2, t1)
    enterTournament(p3, t1)
    enterTournament(p4, t1)
    standings = playerStandings(t1)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, t1)
    reportMatch(id3, id4, t1)
    standings = playerStandings(t1)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    t1 = createTournament("t1")
    p1 = registerPlayer("Twilight Sparkle")
    p2 = registerPlayer("Fluttershy")
    p3 = registerPlayer("Applejack")
    p4 = registerPlayer("Pinkie Pie")
    enterTournament(p1, t1)
    enterTournament(p2, t1)
    enterTournament(p3, t1)
    enterTournament(p4, t1)
    standings = playerStandings(t1)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, t1)
    reportMatch(id3, id4, t1)
    pairings = swissPairings(t1)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."

# Additional tests for extra credit: multiple tournament

def testDeleteTournaments():
    deleteTournaments()
    print "9. Old tournaments can be deleted."
    
    # Check that there are no tournaments in the table
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tournament;")
    count = cursor.fetchall()[0][0]
    dbconn.close()
    if count != 0:
        raise ValueError("After running deleteTournaments(), there should be 0 tournaments.")
    print "10. After running deleteTournament(), there are 0 tournaments."

def testCreateTournament():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament_id = createTournament("Testing tournament")
    
    # Check that createTournament returns an integer ID
    if not isinstance(tournament_id, int):
        raise ValueError("createTournament() should return an integer id.")
    print "11. createTournament() returns an integer id."
    
    # Check that there is now one tournament in the table
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tournament;")
    count = cursor.fetchall()[0][0]
    if count != 1:
        raise ValueError("After running createTournaments(), there should be 1 tournaments.")
    print "12. After running createTournament(), there are 1 tournaments."
    
    createTournament("Testing tournament two")
    
    # Check that there are now two tournament in the table
    cursor.execute("SELECT COUNT(*) FROM tournament;")
    count = cursor.fetchall()[0][0]
    dbconn.close()
    if count != 2:
        raise ValueError("After running createTournaments(), there should be 2 tournaments.")
    print "13. After running createTournament() again, there are 2 tournaments."
    
    # Clean up
    deleteTournaments()

def testEnterTournament():
    # Clean out database
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    
    # Create tournaments, players, and enter players into tournaments
    tournamentA = createTournament("TournamentA")
    tournamentB = createTournament("TournamentA")
    player1_id = registerPlayer("Bob")
    player2_id = registerPlayer("Tim")
    player3_id = registerPlayer("Dave")
    enterTournament(player1_id, tournamentA)
    enterTournament(player2_id, tournamentB)
    enterTournament(player3_id, tournamentB)
    
    # Databse connection
    dbconn = connect()
    cursor = dbconn.cursor()
    
    # Tests on Tournament A
    cursor.execute("""SELECT * FROM player_tournament
                      WHERE tournament_id = %s;""",
                   (tournamentA,))
    rows = cursor.fetchall()
    if len(rows) != 1:
        raise ValueError("There ought to only 1 entrant in Tournament A. There are {0}".format(len(rows)))
    print "14. One entrant added to tournament A"
    if rows[0][0] != player1_id:
        raise ValueError("The id of the player added to Tournament A should be {0}".format(player1_id))
    print "15. Correct player added to tournament A"
    
    # Tests on Tournament B
    cursor.execute("""SELECT * FROM player_tournament
                      WHERE tournament_id = %s;""",
                   (tournamentB,))
    rows = cursor.fetchall()
    if len(rows) != 2:
        raise ValueError("There ought to 2 entrants in Tournament A. There are {0}".format(len(rows)))
    print "16. Two entrants added to tournament B"
    if set([rows[0][0], rows[1][0]]) != set([player2_id, player3_id]):
        raise ValueError("The id values of the players added to Tournament A should be {0} and {1}".format(player2_id, player3_id))
    print "17. Correct players added to tournament B"
    
    # Database cleanup
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    dbconn.close()

def testCountByTournament():
    # Clean out database
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    
    # Create tournaments, and players
    tournamentA = createTournament("TournamentA")
    tournamentB = createTournament("TournamentA")
    player1_id = registerPlayer("Bob")
    player2_id = registerPlayer("Tim")
    player3_id = registerPlayer("Dave")
    
    #Tests
    if countPlayers(tournament=tournamentA):
        raise ValueError("TournamentA should have 0 entrants.")
    if countPlayers(tournament=tournamentB):
        raise ValueError("TournamentB should have 0 entrants.")
    
    enterTournament(player1_id, tournamentA)
    
    if countPlayers(tournament=tournamentA) != 1:
        raise ValueError("TournamentA should have 1 entrants.")
    if countPlayers(tournament=tournamentB):
        raise ValueError("TournamentB should have 0 entrants.")
    
    enterTournament(player2_id, tournamentB)
    
    if countPlayers(tournament=tournamentA) != 1:
        raise ValueError("TournamentA should have 1 entrants.")
    if countPlayers(tournament=tournamentB) != 1:
        raise ValueError("TournamentB should have 1 entrants.")
    
    enterTournament(player3_id, tournamentB)
    
    if countPlayers(tournament=tournamentA) != 1:
        raise ValueError("TournamentA should have 1 entrants.")
    if countPlayers(tournament=tournamentB) != 2:
        raise ValueError("TournamentB should have 2 entrants.")
    
    print "18. countPlayers gives the right numbers for each tournament."
    
    # Database cleanup
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    
# Test deleting matches from tournament (add to several, delete from one, count all)
# Test standings for particular tournament before matches
# Test reporting matches, and check that expected number of matches exist
# Test standings for particular tournaments after matches are reported
# Test that players in reported matches must have entered relevant tournament        
# Test swiss pairings for particular tournament
# Test cascading deletes
    
if __name__ == '__main__':
    print "Original tests, modified where applicable to account for extra-credit changes:"
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()    # Modified for tournament paramter
    testReportMatches()             # Modified for tournament paramter
    testPairings()                  # Modified for tournament paramter
    
    # Tests for extra credit: multiple tournaments
    print "\nNew tests for extra credit option: multiple tournaments:"
    testDeleteTournaments()
    testCreateTournament()
    testEnterTournament()
    testCountByTournament()
    print "\nSuccess!  All tests pass!"


