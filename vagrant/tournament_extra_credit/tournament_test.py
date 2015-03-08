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
    # Modified to work with a database allowing multiple tournaments
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    p1 = registerPlayer("Melpomene Murray")
    p2 = registerPlayer("Randy Schwartz")
    t1 = createTournament("t1")
    
    # Test that standings are empty before players enter tournaments
    standings = playerStandings(t1)
    if len(standings) != 0:
        raise ValueError("Players should not appear in a tournament's standings before they have entered any tournaments")
    print "6. Players do not appear in a tournament's standings before they enter a tournament"
    
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
    print "7. Newly registered players appear in the standings with no matches."


def testReportMatches():
    # Modified to work with a database allowing multiple tournaments
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
    print "8. After a match, players have updated standings."


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
    print "9. After one match, players with one win are paired."

# Additional tests for extra credit: multiple tournament

def testDeleteTournaments():
    deleteTournaments()
    print "10. Old tournaments can be deleted."
    
    # Check that there are no tournaments in the table
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tournament;")
    count = cursor.fetchall()[0][0]
    dbconn.close()
    if count != 0:
        raise ValueError("After running deleteTournaments(), there should be 0 tournaments.")
    print "11. After running deleteTournament(), there are 0 tournaments."

def testCreateTournament():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament_id = createTournament("Testing tournament")
    
    # Check that createTournament returns an integer ID
    if not isinstance(tournament_id, int):
        raise ValueError("createTournament() should return an integer id.")
    print "12. createTournament() returns an integer id."
    
    # Check that there is now one tournament in the table
    dbconn = connect()
    cursor = dbconn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tournament;")
    count = cursor.fetchall()[0][0]
    if count != 1:
        raise ValueError("After running createTournaments(), there should be 1 tournaments.")
    print "13. After running createTournament(), there are 1 tournaments."
    
    createTournament("Testing tournament two")
    
    # Check that there are now two tournament in the table
    cursor.execute("SELECT COUNT(*) FROM tournament;")
    count = cursor.fetchall()[0][0]
    dbconn.close()
    if count != 2:
        raise ValueError("After running createTournaments(), there should be 2 tournaments.")
    print "14. After running createTournament() again, there are 2 tournaments."
    
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
    print "15. One entrant added to tournament A"
    if rows[0][0] != player1_id:
        raise ValueError("The id of the player added to Tournament A should be {0}".format(player1_id))
    print "16. Correct player added to tournament A"
    
    # Tests on Tournament B
    cursor.execute("""SELECT * FROM player_tournament
                      WHERE tournament_id = %s;""",
                   (tournamentB,))
    rows = cursor.fetchall()
    if len(rows) != 2:
        raise ValueError("There ought to 2 entrants in Tournament A. There are {0}".format(len(rows)))
    print "17. Two entrants added to tournament B"
    if set([rows[0][0], rows[1][0]]) != set([player2_id, player3_id]):
        raise ValueError("The id values of the players added to Tournament A should be {0} and {1}".format(player2_id, player3_id))
    print "18. Correct players added to tournament B"
    
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
    
    print "19. countPlayers gives the right numbers for each tournament."
    
    # Database cleanup
    deleteMatches()
    deletePlayers()
    deleteTournaments()

def testStandingsBeforeMatchesByTournament():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    p1 = registerPlayer("Melpomene Murray")
    p2 = registerPlayer("Randy Schwartz")
    p3 = registerPlayer("Bob, son of Tim")
    t1 = createTournament("t1")
    t2 = createTournament("t2")
    
    # Test that standings are empty before players enter tournaments
    standings_t1 = playerStandings(t1)
    standings_t2 = playerStandings(t2)
    if len(standings_t1) != 0 or len(standings_t2) != 0:
        raise ValueError("Players should not appear in a tournament's standings before they have entered any tournaments")
    print "20. Players do not appear in a tournament's standings before they enter a tournament"
    
    enterTournament(p1, t1)
    enterTournament(p2, t1)
    enterTournament(p2, t2)
    enterTournament(p3, t2)
    
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
    
    standings = playerStandings(t2)
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
    if set([name1, name2]) != set(["Randy Schwartz", "Bob, son of Tim"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    
    print "21. Newly registered players appear in the standings with no matches, for any tournaments entered."

def testReportMatchesByTournament():
    # Modified to work with a database allowing multiple tournaments
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    t1 = createTournament("t1")
    t2 = createTournament("t2")
    p1 = registerPlayer("Bruno Walton")
    p2 = registerPlayer("Boots O'Neal")
    p3 = registerPlayer("Cathy Burton")
    p4 = registerPlayer("Diane Grant")
    p5 = registerPlayer("Bob, son of Tim")
    p6 = registerPlayer("Ted, son of Ed")
    enterTournament(p1, t1)
    enterTournament(p2, t1)
    enterTournament(p3, t1)
    enterTournament(p4, t1)
    enterTournament(p2, t2)
    enterTournament(p3, t2)
    enterTournament(p4, t2)
    enterTournament(p5, t2)
    
    reportMatch(p1, p2, t1)
    reportMatch(p3, p4, t1)
    
    reportMatch(p3, p4, t2)
    reportMatch(p5, p2, t2)
    
    # Test that matches can only be reported where the players have already entered the tournament
    try:
        reportMatch(p5, p6, t1)
    except psycopg2.InternalError as e:
        if not e.message.startswith("Attempted to record match involving player"):
            raise
        else:
            print "22. Database stops attempts to record matches with participants who have not entered relevant tournament"
    
    if len(getMatches(t1)) != 2 or len(getMatches(t2)) != 2:
        raise ValueError("There should be two matches in each tournament")
    
    for (i, n, w, m) in playerStandings(t1):
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (p1, p3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (p2, p4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    
    for (i, n, w, m) in playerStandings(t2):
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (p3, p5) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (p4, p2) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    
    # Database cleanup
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    
    print "23. After a match, players have updated standings for the relevant tournament."

# Test standings for particular tournaments after matches are reported      
# Test swiss pairings for particular tournament
# Test cascading deletes

# Test deleting matches from tournament (add to several, delete from one, count all)
    
if __name__ == '__main__':
    print "\nOriginal tests, modified where applicable to account for extra-credit changes:"
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
    testStandingsBeforeMatchesByTournament()
    testReportMatchesByTournament()
    print "\nSuccess!  All tests pass!"


