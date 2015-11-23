-- part of the tournament project for the Udacity course "Intro to Relational Databases"
-- https://www.udacity.com/course/viewer#!/c-ud197
-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- if necessary:
-- drop database tournament;

create database tournament;

create table players (
  name  text,
  id    serial PRIMARY KEY
);

create table games (
  round   int NOT NULL,
  winner  int REFERENCES players (id),
  loser   int REFERENCES players (id),
  CONSTRAINT game_ident PRIMARY KEY(round, winner, loser),
  CONSTRAINT no_games_against_self CHECK (winner != loser)
);
  -- players must not be the same; primary key: round,w,l
  -- could do ON DELETE CASCADE to maintain integrity

-- Example:
-- insert into players values ('Mike');
-- insert into players values ('John');
-- insert into games values (1, 1, 2);

-- fails: insert into games values (1, 1, 2); due to game_ident
-- fails: insert into games values (1, 1, 1); due to no_games_against_self


CREATE VIEW wincount AS
SELECT players.id, players.name, count(games.winner) as wins
  FROM players LEFT JOIN games
  ON players.id = games.winner
  GROUP BY players.id
  ORDER BY wins DESC;

CREATE VIEW losscount AS
  SELECT players.id, players.name, count(games.loser) as losses
    FROM players LEFT JOIN games
    ON players.id = games.loser
    GROUP BY players.id
    ORDER BY losses;

CREATE VIEW standing AS
SELECT id, name, wins, (wins+losses) as matches
  FROM wincount NATURAL JOIN losscount
  ORDER BY wins DESC;
