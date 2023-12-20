DROP TABLE Cricket_Players;
DROP TABLE Cricket_Games;
DROP TABLE Cricket_Tournaments;
DROP TABLE Cricket_Teams;


-- Table for available teams
CREATE TABLE Cricket_Teams (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(15) NOT NULL,
    total_players INT,
    wins INT
);

-- Table for tournaments
CREATE TABLE Cricket_Tournaments (
    tournament_id INT PRIMARY KEY,
    tournament_name VARCHAR(15) NOT NULL,
    winner_id INT,
    total_teams INT,
    FOREIGN KEY (winner_id) REFERENCES Cricket_Teams(team_id)
);

-- Table for games played
CREATE TABLE Cricket_Games (
    game_id INT PRIMARY KEY,
    tournament_id INT,
    team1_id INT,
    team2_id INT,
    winner_id INT,
    FOREIGN KEY (tournament_id) REFERENCES Cricket_Tournaments(tournament_id),
    FOREIGN KEY (team1_id) REFERENCES Cricket_Teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES Cricket_Teams(team_id),
    FOREIGN KEY (winner_id) REFERENCES Cricket_Teams(team_id)
);

-- Table for players
CREATE TABLE Cricket_Players (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(15) NOT NULL,
    team_id INT,
    jersey_no INT,
    no_matches_played INT,
    FOREIGN KEY (team_id) REFERENCES Cricket_Teams(team_id)
);


REM PLSQL
CREATE OR REPLACE FUNCTION 
find_team_id(p_id NUMBER)
RETURN NUMBER 
IS
required_id NUMBER := 0;
BEGIN

    SELECT team_id INTO required_id 
    FROM Cricket_Players
    WHERE player_id = p_id;

    RETURN required_id;
END;
/

CREATE OR REPLACE TRIGGER 
check_total_teams
BEFORE INSERT OR UPDATE
ON Cricket_Tournaments
FOR EACH ROW
DECLARE
    total_teams_var int := 0;
BEGIN
    SELECT COUNT(*) INTO total_teams_var
    FROM Cricket_Teams;
    IF total_teams_var < :NEW.total_teams THEN
        RAISE_APPLICATION_ERROR(-20001, 'Invalid Total Players');
    END IF;
END;
/

-- Function to find the name of a player when his/her id is given
CREATE OR REPLACE FUNCTION 
find_player_name(p_id NUMBER)
RETURN VARCHAR2
IS
required_name varchar2(30);
BEGIN
    SELECT player_name INTO required_name FROM Cricket_Players
    WHERE player_id = p_id;

    RETURN required_name;
END;
/

-- Function to find team name when Team id is given.
CREATE OR REPLACE FUNCTION 
find_team_name(t_id NUMBER)
RETURN VARCHAR2
IS
required_name varchar2(30);
BEGIN
    SELECT team_name INTO required_name FROM Cricket_Teams
    WHERE team_id = t_id;

    RETURN required_name;
END;
/

-- Function to find the name of a tournament when id is given
CREATE OR REPLACE FUNCTION 
find_tournament_name(t_id NUMBER)
RETURN VARCHAR2
IS
required_name varchar2(30);
BEGIN
    SELECT tournament_name INTO required_name FROM Cricket_Tournaments
    WHERE tournament_id = t_id;

    RETURN required_name;
END;
/

--Sequence for Tournament Number!
CREATE SEQUENCE cric_tour_number
START WITH 1
INCREMENT BY 1
MAXVALUE 999999
CYCLE
CACHE 20; 

--Trigger for checking count of players in a cricket team.
CREATE OR REPLACE TRIGGER
trg_count_players
BEFORE INSERT OR UPDATE
ON Cricket_Teams
FOR EACH ROW
BEGIN
    IF :NEW.total_players > 25 THEN 
        RAISE_APPLICATION_ERROR(-20001, 'Cannot have a team with more than 11 Players.');
    ELSIF :NEW.total_players < 11 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Cannot have a team with players less than 8 Players.');
    END IF;
END;
/


-- INserting Values into teams Table!
INSERT INTO Cricket_Teams (team_id, team_name, total_players, wins) VALUES (1, 'Team1', 15, 5);
INSERT INTO Cricket_Teams (team_id, team_name, total_players, wins) VALUES (2, 'Team2', 11, 3);


-- Inserting values into the players table
INSERT INTO Cricket_Players (player_id, player_name, team_id, jersey_no, no_matches_played) VALUES (1, 'Player1', 1, 10, 20);
INSERT INTO Cricket_Players (player_id, player_name, team_id, jersey_no, no_matches_played) VALUES (2, 'Player2', 1, 7, 15);
INSERT INTO Cricket_Players (player_id, player_name, team_id, jersey_no, no_matches_played) VALUES (3, 'Player3', 2, 5, 18);

-- Inserting values into the tournaments table
INSERT INTO Cricket_Tournaments (tournament_id, tournament_name, winner_id, total_teams) VALUES (1, 'Tournament1', 1, 2);
INSERT INTO Cricket_Tournaments (tournament_id, tournament_name, winner_id, total_teams) VALUES (2, 'Tournament2', 2, 2);

-- Inserting values into the games table
INSERT INTO Cricket_Games (game_id, tournament_id, team1_id, team2_id, winner_id) VALUES (1, 1, 1, 2, 1);
INSERT INTO Cricket_Games (game_id, tournament_id, team1_id, team2_id, winner_id) VALUES (2, 1, 2, 1, 2);
INSERT INTO Cricket_Games (game_id, tournament_id, team1_id, team2_id, winner_id) VALUES (3, 2, 1, 2, 2);



