DROP TABLE Cricket_Teams;
DROP TABLE Cricket_Team_Players;


CREATE TABLE Cricket_Teams(
	TEAM_NAME varchar(50) PRIMARY KEY,
	COLOUR varchar(20)
);

CREATE TABLE Cricket_Team_Players(
	TEAM_NAME varchar(20),
	PLAYER_ID int,
	PLAYER_NAME varchar(50),
	STATUS varchar(10)
);

ALTER TABLE Cricket_Team_Players
ADD CONSTRAINT CHK_NAME_CRIC_FK 
FOREIGN KEY (TEAM_NAME) REFERENCES Cricket_Teams(TEAM_NAME);


