# Third-party code credits

In vagrant/tournament_extra_credit/tournament.sql:
 - The sql function check_match_tournament_membership() and related trigger were created using the code in the following document as a starting point: [http://www.postgresql.org/docs/9.0/static/plpgsql-trigger.html](http://www.postgresql.org/docs/9.0/static/plpgsql-trigger.html)

In vagrant/tournament_extra_credit/tournament_test.py
 - Many of the additional tests are based on tests in the original file provided.
    - testStandingsBeforeMatchesByTournament() is based on testStandingsBeforeMatches()
    - testReportMatchesByTournament() is based on testReportMatches().
    - testPlayerStandings() is based on testReportMatches().
    - testPairingByTournament() is based on testPairings().
