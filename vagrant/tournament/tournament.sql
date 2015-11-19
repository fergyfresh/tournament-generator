-- Table definitions for the tournament project.
--
-- To initialize:
-- createdb tournament
-- psql tournament

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players  ( id serial PRIMARY KEY,
                        name varchar (25) NOT NULL,
                        created_at timestamp default current_timestamp );

CREATE TABLE matches  ( id serial PRIMARY KEY,
                        winner_id int,
                        loser_id int,
                        foreign key (winner_id) references players(id),
                        foreign key (loser_id) references players(id) );
