-- -----------------------------------------------------
-- Drop the 'heating' database/schema
-- -----------------------------------------------------

DROP SCHEMA IF EXISTS heating;

-- -----------------------------------------------------
-- Create 'inventory' database/schema and use this database
-- -----------------------------------------------------

CREATE SCHEMA IF NOT EXISTS heating;


USE heating;




-- -----------------------------------------------------
-- Drop tables
-- -----------------------------------------------------

-- drop table data_values;

-- -----------------------------------------------------
-- Create table data_values
-- -----------------------------------------------------

CREATE TABLE if not EXISTS test (
    ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    flueGas FLOAT,
    boilerTemp FLOAT,
    bufferTop FLOAT,
    bufferMid FLOAT,
    bufferBottom FLOAT,
    hotWater FLOAT,
    woodFan INT,
    woodCircPump INT,
    woodHeatCircPump INT,
    oilBoiler INT,
    hotWaterValve INT,
    switchOver INT,
    startButton INT,
    commsEstablished INT,
    `timeStamp` VARCHAR(255)
);
DROP TABLE test;


INSERT INTO test (flueGas,boilerTemp,bufferTop,bufferMid,bufferBottom,hotWater,woodFan,woodCircPump,woodHeatCircPump,oilBoiler,
hotWaterValve,switchOver,startButton,`timeStamp`)
	VALUES (1,2,3,4,5,6,7,8,9,10,11,12,13,14);

SELECT  boilerTemp,bufferTop,bufferMid,bufferBottom,hotWater, from_unixtime(timestamp, '%d %m %Y %H:%i:%s') FROM test ORDER BY id DESC LIMIT 20;

SELECT * FROM test;
SELECT from_unixtime(timestamp, '%d %m %Y %H:%i:%s'),flueGas, boilerTemp, bufferTop, bufferMid, bufferBottom, hotWater FROM test ORDER BY ID DESC LIMIT 1;

USE heating;
SELECT from_unixtime(timestamp, '%d %m %Y %H:%i:%s'),flueGas, boilerTemp, bufferTop, bufferMid, bufferBottom, hotWater FROM test WHERE ID = 430;

SELECT
 from_unixtime(timestamp, '%D %m %Y %H:%i:%s') AS Time
FROM 
heating.startbutton;

-- --------------------------------------------
CREATE OR REPLACE VIEW last_25 AS
    SELECT 
        FROM_UNIXTIME(timestamp, '%d %m %Y %H:%i:%s'),
        flueGas,
        boilerTemp,
        bufferTop,
        bufferMid,
        bufferBottom,
        hotWater
    FROM
        test
    ORDER BY ID DESC
    LIMIT 20;


