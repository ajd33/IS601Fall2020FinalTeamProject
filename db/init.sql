CREATE DATABASE fordEscort;
use fordEscort;

CREATE TABLE IF NOT EXISTS escort (
    `id` INT NOT NULL AUTO_INCREMENT,
    `Year` INT,
    `Mileage` INT,
    `Price` INT,
    `Column_4` VARCHAR(10) CHARACTER SET utf8,
    PRIMARY KEY (id)
);
INSERT INTO escort (`Year`,`Mileage`,`Price`,`Column_4`) VALUES
    (1998,27000,9991,NULL),
