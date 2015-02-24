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
    player1_id INTEGER REFERENCES player (id),
    player2_id INTEGER REFERENCES player (id),
    winner_id INTEGER NULL REFERENCES player (id)   -- So that draws can be recorded as null (not yet used)
        CHECK (                                     -- constraint so winner must one of the players
            winner_id = player1_id
            or winner_id = player2_id 
            or winner_id IS NULL 
        ),
    tournament_id INTEGER REFERENCES tournament (id),   -- TO DO: Modify so that players must be entrants to tournament
    PRIMARY KEY (player1_id, player2_id),           -- constraints to ensure that...
    CHECK (player1_id < player2_id)                 -- ...players are matched only once
); 

-- Creates many-to-many relationship between players and tournaments                          
CREATE TABLE player_tournament (
    player_id INTEGER REFERENCES player (id),
    tournament_id INTEGER REFERENCES tournament (id),
    PRIMARY KEY (player_id, tournament_id)
);
                                 

-- Views:

-- Used as an input to loss_count.
--
--  player1_id | player2_id | loser_id 
-- ------------+------------+----------
--
--CREATE VIEW match_loser AS
--    SELECT player1_id,
--           player2_id,
--           CASE -- selects the id of the losing player
--                WHEN winner_id = player1_id THEN player2_id
--                WHEN winner_id = player2_id THEN player1_id
--                WHEN winner_id IS NULL THEN NULL
--           END AS loser_id
--    FROM match;


-- Used as input to player_standing
--
--  winner_id | num_matches_won 
-- -----------+-----------------
--
--CREATE VIEW win_count AS 
--    SELECT player.id as winner_id,
--           COUNT(match.winner_id) as num_matches_won
--    FROM player LEFT JOIN match -- has to be a left join to get zero values
--    ON player.id = match.winner_id
--    GROUP BY player.id;


-- Used as input to player_standing
--
--  loser_id | num_matches_lost 
-- ----------+------------------
--
--CREATE VIEW loss_count AS 
--    SELECT player.id as loser_id,
--           COUNT(match_loser.loser_id) as num_matches_lost
--    FROM player LEFT JOIN match_loser -- has to be a left join to get zero values
--    ON player.id = match_loser.loser_id
--    GROUP BY player.id;


-- Used as input to player_standing
--
--  player_id | num_matches 
-- -----------+-------------
--
--CREATE VIEW match_count AS
--    SELECT player.id AS player_id,
--           COUNT(player1_id) as num_matches 
--    FROM player LEFT JOIN match
--    ON player.id = player1_id OR player.id = player2_id
--    GROUP BY player.id;


--  player_id |  name  | win_count | lose_count | match_count 
-- -----------+--------+-----------+------------+-------------
--
--CREATE VIEW player_standing AS
--    SELECT winner_id as player_id,
--           player.name,
--           win_count.num_matches_won as win_count,
--           loss_count.num_matches_lost as lose_count,
--           match_count.num_matches as match_count
--    FROM win_count
--        JOIN loss_count
--            ON winner_id = loser_id
--        JOIN player
--            ON winner_id = player.id
--        JOIN match_count
--            ON winner_id = match_count.player_id
--    ORDER BY win_count;


-- Used as input to swiss_pairings
--CREATE VIEW numbered_standing AS
--    SELECT 
--        ROW_NUMBER() OVER(ORDER BY win_count DESC) as row,
--        ROW_NUMBER() OVER(ORDER BY win_count DESC) % 2 = 0 as even_row,
--        * 
--    FROM player_standing;


-- Takes players ordered by number of wins, and pairs the player in
-- row 1 with that in row 2, row 3 with row 4, row 5 with row 6 etc.
--
--  id1 | name1  | id2 |   name2    
-- -----+--------+-----+------------
--
--CREATE VIEW swiss_pairing AS
--    SELECT
--        a.player_id as id1, 
--        a.name as name1, 
--        b.player_id as id2, 
--        b.name as name2
--    FROM 
--        (SELECT * FROM numbered_standing WHERE even_row = FALSE) AS a 
--        JOIN
--        (SELECT * FROM numbered_standing WHERE even_row = TRUE) AS b
--        ON a.row = b.row - 1;

