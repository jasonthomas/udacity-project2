-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- player table
CREATE TABLE player (
    id serial primary key,
    name varchar(255)
);

-- match table
CREATE TABLE match (
    id serial primary key,
    winner int references player(id) ON DELETE CASCADE,
    loser int references player(id) ON DELETE CASCADE
);

-- wins view
CREATE VIEW v_wins as SELECT player.id, player.name, count(match.winner) as wins
FROM player LEFT JOIN match
ON player.id = match.winner
GROUP BY player.id;

-- losses view
CREATE VIEW v_losses as SELECT player.id, player.name, count(match.winner) as losses
FROM player LEFT JOIN match
ON player.id = match.loser
GROUP BY player.id;

-- totalmatches view
-- view based on wins and losses view
CREATE VIEW v_totalmatches as SELECT v_wins.id, v_wins.name, v_wins.wins + v_losses.losses as matches
FROM v_wins, v_losses
WHERE v_wins.id = v_losses.id;

-- standings view
-- view based on wins and totalmatches views
CREATE VIEW standing as SELECT v_wins.id, v_wins.name, v_wins.wins, v_totalmatches.matches
FROM v_wins, v_totalmatches
WHERE v_wins.id = v_totalmatches.id
ORDER BY v_wins.wins desc;
