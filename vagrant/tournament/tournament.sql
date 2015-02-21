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
                       winner_id INTEGER NULL REFERENCES players (id), -- So that draws can be recorded as null
                       PRIMARY KEY (player1_id, player2_id),
                       CHECK (player1_id < player2_id) ); -- constraints to ensure that players are matched only once
