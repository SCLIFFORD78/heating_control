-- -----------------------------------------------------
-- Drop the 'mqtt' database/schema
-- -----------------------------------------------------

DROP SCHEMA IF EXISTS mqtt;
-- -----------------------------------------------------
-- Create 'inventory' database/schema and use this database
-- -----------------------------------------------------

CREATE SCHEMA IF NOT EXISTS mqtt;

USE mqtt;

-- -----------------------------------------------------
-- Drop tables
-- -----------------------------------------------------

-- drop table data_values;

-- -----------------------------------------------------
-- Create table data_values
-- -----------------------------------------------------

CREATE TABLE flueGas
(
    ID          INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    flueGas     FLOAT,
    `timeStamp` VARCHAR(255)
);

CREATE TABLE boilerTemp
(
    ID          INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    boilerTemp  FLOAT,
    `timeStamp` VARCHAR(255)
);

CREATE TABLE bufferTop
(
    ID          INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    bufferTop   FLOAT,
    `timeStamp` VARCHAR(255)
);

CREATE TABLE bufferMid
(
    ID          INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    bufferMid   FLOAT,
    `timeStamp` VARCHAR(255)
);

CREATE TABLE hotWater
(
    ID          INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    hotWater    FLOAT,
    `timeStamp` VARCHAR(255)
);

CREATE TABLE bufferBottom
(
	ID          INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    bufferBottom FLOAT,
    `timeStamp`  VARCHAR(255)
);

CREATE TABLE heartBeat
(
    ID          INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    heartBeat   INT,
    `timeStamp` VARCHAR(255)
);

CREATE TABLE woodFan
(
	ID          INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    woodFan     INT,
    `timeStamp` VARCHAR(255)
);


CREATE TABLE woodCircPump
(
    ID           INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    woodCircPump INT,
    `timeStamp`  VARCHAR(255)
);

CREATE TABLE woodHeatCircPump
(
    ID               INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    woodHeatCircPump INT,
    `timeStamp`      VARCHAR(255)
);

CREATE TABLE oilBoiler
(
	ID          INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    oilBoiler   INT,
    `timeStamp` VARCHAR(255)
);

CREATE TABLE hotWaterValve
(
    ID            INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    hotWaterValve INT,
    `timeStamp`   VARCHAR(255)
);

CREATE TABLE switchOver
(
	ID          INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    switchOver  INT,
    `timeStamp` VARCHAR(255)
);



CREATE TABLE startButton
(
    ID          INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    startButton INT,
    `timeStamp` VARCHAR(255)
);

SELECT
 from_unixtime(timestamp, '%D %m %Y %H:%i:%s') AS Time
FROM 
mqtt.startbutton;

-- --------------------------------------------




