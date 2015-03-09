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
                       
CREATE TABLE match ( 
    player1_id INTEGER REFERENCES player (id),
    player2_id INTEGER REFERENCES player (id),
    winner_id INTEGER NULL REFERENCES player (id)   -- So that draws can be recorded as null (not yet used)
        CHECK (                                     -- constraint so winner must one of the players
            winner_id = player1_id
            or winner_id = player2_id 
            or winner_id IS NULL
        ),       
    PRIMARY KEY (player1_id, player2_id),           -- constraints to ensure that...
    CHECK (player1_id < player2_id)                 -- ...players are matched only once
);


-- Views:

-- Used as input to player_standing
--
--  winner_id | num_matches_won 
-- -----------+-----------------
--
CREATE VIEW win_count AS 
    SELECT player.id as winner_id,
           COUNT(match.winner_id) as num_matches_won
    FROM player LEFT JOIN match -- has to be a left join to get zero values
    ON player.id = match.winner_id
    GROUP BY player.id;


-- Used as input to player_standing
--
--  player_id | num_matches 
-- -----------+-------------
--
CREATE VIEW match_count AS
    SELECT player.id AS player_id,
           COUNT(player1_id) as num_matches 
    FROM player LEFT JOIN match
    ON player.id = player1_id OR player.id = player2_id
    GROUP BY player.id;


--  player_id |  name  | win_count | match_count 
-- -----------+--------+-----------+-------------
--
CREATE VIEW player_standing AS
    SELECT winner_id as player_id,
           player.name,
           win_count.num_matches_won as win_count,
           match_count.num_matches as match_count
    FROM win_count
        JOIN player
            ON winner_id = player.id
        JOIN match_count
            ON winner_id = match_count.player_id
    ORDER BY win_count DESC;

