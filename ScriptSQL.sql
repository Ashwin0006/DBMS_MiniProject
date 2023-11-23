DROP TABLE Cricket_Teams;
DROP TABLE Cricket_Team_Players;


CREATE TABLE Cricket_Teams(
	TEAM_NAME varchar(50) PRIMARY KEY,
	COLOUR varchar(20)
);

CREATE TABLE Cricket_Team_Players(
	PLAYER_ID int PRIMARY KEY,
	PLAYER_NAME varchar(50),
	STATUS varchar(10)
);


