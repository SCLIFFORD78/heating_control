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
SELECT from_unixtime(timestamp, '%d %m %Y %H:%i:%s'),flueGas, boilerTemp, bufferTop, bufferMid, bufferBottom, hotWater FROM test WHERE ID = 2680;

SELECT
 from_unixtime(timestamp, '%D %m %Y %H:%i:%s') AS Time
FROM 
heating.startbutton;

SELECT from_unixtime(timestamp, '%D %m %Y %H:%i:%s') AS Time from heating.test WHERE woodFan = 0;

SELECT avg(bufferTop) from test where `timestamp` between ((SELECT `timestamp` FROM test ORDER BY id DESC LIMIT 1)-300)  and (SELECT `timestamp` FROM test ORDER BY id DESC LIMIT 1);

DROP procedure IF EXISTS heating.repeat_loop_example;

DROP TABLE IF EXISTS results;
delimiter //

CREATE procedure heating.repeat_loop_example()
wholeblock:BEGIN
  DECLARE x INT;
  DECLARE averages FLOAT;
  SET x = 0;
DROP TABLE IF EXISTS results;
CREATE TABLE IF NOT EXISTS results (
    ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    buffertop FLOAT,
    timestamp_ VARCHAR(255)
);

  REPEAT
  INSERT INTO results (bufferTop, timestamp_)
  VALUES(
	(SELECT avg(bufferTop) from test where `timestamp` between ((SELECT `timestamp` FROM test ORDER BY id DESC LIMIT 1)-(x+300))  and ((SELECT `timestamp` FROM test ORDER BY id DESC LIMIT 1)-x)),
	(SELECT `timestamp` FROM test ORDER BY id DESC LIMIT 1)-x 
    );

    SET x = x + 300;
    UNTIL x >= 6000
  END REPEAT;


END//

USE heating;

call repeat_loop_example();

SELECT bufferTop,from_unixtime(timestamp_, '%d %m %Y %H:%i:%s') AS time_ from results order by time_;




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


