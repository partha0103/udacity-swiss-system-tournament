-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players ( id SERIAL PRIMARY KEY,
                       name TEXT );
                       
CREATE TABLE matches ( player1_id INTEGER REFERENCES players (id),
                       player2_id INTEGER REFERENCES players (id),
                       winner_id INTEGER NULL REFERENCES players (id), -- So that draws can be recorded as null, not yet used
                       PRIMARY KEY (player1_id, player2_id),
                       CHECK (player1_id < player2_id) ); -- constraints to ensure that players are matched only once

CREATE VIEW matches_winners_losers AS
    SELECT player1_id,
           player2_id,
           winner_id,
           CASE 
                WHEN winner_id = player1_id THEN player2_id
                WHEN winner_id = player2_id THEN player1_id
                WHEN winner_id IS NULL THEN NULL
           END AS loser_id
    FROM matches;

CREATE VIEW wins AS 
    SELECT players.id as winner_id,
           COUNT(matches.winner_id)
    FROM players LEFT JOIN matches -- has to be a left join to get zero values
    ON players.id = matches.winner_id
    GROUP BY players.id;

CREATE VIEW losses AS 
    SELECT players.id as loser_id,
           COUNT(matches_winners_losers.loser_id)
    FROM players LEFT JOIN matches_winners_losers -- has to be a left join to get zero values
    ON players.id = matches_winners_losers.loser_id
    GROUP BY players.id;

CREATE VIEW matches_count AS
    SELECT players.id AS player_id,
           COUNT(player1_id) 
    FROM players LEFT JOIN matches
    ON players.id = player1_id OR players.id = player2_id
    GROUP BY players.id;

CREATE VIEW player_standings AS
    SELECT winner_id as player_id,
           players.name,
           wins.count as win_count,
           losses.count as lose_count,
           matches_count.count as match_count
    FROM wins
        JOIN losses
        ON winner_id = loser_id
        JOIN players
        ON winner_id = players.id
        JOIN matches_count
        ON winner_id = matches_count.player_id;
