-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players(
	id SERIAL PRIMARY KEY,
    name text NOT NULL,
	num_wins INT DEFAULT 0,
	num_matches INT DEFAULT 0
   
);

CREATE TABLE matches(
    match_id SERIAL PRIMARY KEY,
    winner INT DEFAULT 0,
    loser INT DEFAULT 0
);

CREATE VIEW wins_view AS SELECT id, name, num_wins, num_matches
	FROM players ORDER BY num_wins DESC;