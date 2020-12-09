CREATE DATABASE gasMileage;
use gasMileage;

CREATE TABLE IF NOT EXISTS mileage (
    `id` INT NOT NULL AUTO_INCREMENT,
    `Gallons` INT,
    `Miles Driven` INT,
    `Cost` INT,
    `Column_4` VARCHAR(10) CHARACTER SET utf8,
    PRIMARY KEY (id)
);
INSERT INTO escort (`Year`,`Mileage`,`Price`,`Column_4`) VALUES
    (12.2,300,,NULL),
    (11.9,270,21.22,NULL),
    (12.4,320,20.51,NULL),
