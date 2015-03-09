-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Tables:

CREATE TABLE player (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE tournament (
    id SERIAL PRIMARY KEY,
    name TEXT 
);

-- TO DO: Modify so that matches are linked to a tournament                       
CREATE TABLE match ( 
    player1_id INTEGER REFERENCES player (id) ON DELETE CASCADE, -- If player1 is deleted, their matches will be deleted
    player2_id INTEGER REFERENCES player (id) ON DELETE CASCADE, -- If player2 is deleted, their matches will be deleted
    winner_id INTEGER NULL REFERENCES player (id)   -- So that draws can be recorded as null (not yet used)
        CHECK (                                     -- constraint so winner must one of the players
            winner_id = player1_id
            or winner_id = player2_id 
            or winner_id IS NULL 
        ),
    tournament_id INTEGER REFERENCES tournament (id) ON DELETE CASCADE,   -- TO DO: Modify so that players must be entrants to tournament
    PRIMARY KEY (player1_id, player2_id, tournament_id),           -- constraints to ensure that...
    CHECK (player1_id < player2_id)                 -- ...players are matched only once
); 

-- Creates many-to-many relationship between players and tournaments                          
CREATE TABLE player_tournament (
    player_id INTEGER REFERENCES player (id) ON DELETE CASCADE, -- If a player is deleted, the row linking them to a tournament is deleted
    tournament_id INTEGER REFERENCES tournament (id) ON DELETE CASCADE, -- If a tournament is deleted, their rows are deleted
    PRIMARY KEY (player_id, tournament_id)
);

CREATE FUNCTION check_match_tournament_membership() RETURNS trigger AS $check_match_tournament_membership$
    BEGIN
        IF NEW.player1_id NOT IN (SELECT player_id FROM player_tournament WHERE tournament_id = NEW.tournament_id) THEN
            RAISE EXCEPTION 'Attempted to record match involving player % who is not a participant in tournament %.', 
                NEW.player1_id, 
                NEW.tournament_id;
        END IF;
        IF NEW.player2_id NOT IN (SELECT player_id FROM player_tournament WHERE tournament_id = NEW.tournament_id) THEN
            RAISE EXCEPTION 'Attempted to record match involving player % who is not a participant in tournament %.', 
                NEW.player2_id, 
                NEW.tournament_id;
        END IF;
    RETURN NEW;
    END;
$check_match_tournament_membership$ LANGUAGE plpgsql;

CREATE TRIGGER check_match_tournament_membership BEFORE INSERT OR UPDATE ON match
    FOR EACH ROW EXECUTE PROCEDURE check_match_tournament_membership();

-- Views:

-- Used for countPlayers()
CREATE VIEW players_per_tournament AS
    SELECT
        tournament.id as tournament_id,
        COUNT(player_tournament.player_id) as num_players
    FROM
        tournament LEFT JOIN player_tournament
            ON tournament.id = player_tournament.tournament_id
    GROUP BY
        tournament.id;


-- Used as input to player_standing
--
--  player_id | tournament_id | num_wins 
-- -----------+---------------+----------
--
CREATE VIEW win_count AS
    SELECT
        player.id as player_id,
        player_tournament.tournament_id as tournament_id,
        COUNT(match.winner_id) as num_wins
    FROM 
        player 
            LEFT JOIN player_tournament
                ON player.id = player_tournament.player_id
            LEFT JOIN match
                ON 
                    player.id = match.winner_id 
                    AND player_tournament.tournament_id = match.tournament_id
    GROUP BY
        player_tournament.tournament_id,
        player.id
    ORDER BY player_id, tournament_id;


-- Used as input to player_standing
--
--  player_id | tournament_id | num_matches 
-- -----------+---------------+-------------
--
CREATE VIEW match_count AS
    SELECT
        player.id as player_id,
        player_tournament.tournament_id as tournament_id,
        COUNT(match.player1_id) as num_matches
    FROM 
        player 
            LEFT JOIN player_tournament
                ON player.id = player_tournament.player_id
            LEFT JOIN match
                ON 
                    (player.id = match.player1_id OR player.id = match.player2_id)
                    AND player_tournament.tournament_id = match.tournament_id
    GROUP BY
        player_tournament.tournament_id,
        player.id
    ORDER BY player_id, tournament_id;


--  player_id |  name   | win_count | match_count | tournament_id 
-- -----------+---------+-----------+-------------+---------------
--
CREATE VIEW player_standing AS
    SELECT player.id as player_id,
           player.name,
           win_count.num_wins as win_count,
           match_count.num_matches as match_count,
           match_count.tournament_id
    FROM player
        JOIN win_count
            ON win_count.player_id = player.id
        JOIN match_count
            ON win_count.player_id = match_count.player_id
            AND win_count.tournament_id = match_count.tournament_id
    ORDER BY tournament_id, win_count DESC;

