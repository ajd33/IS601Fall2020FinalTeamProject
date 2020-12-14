CREATE DATABASE gasMileage;
use gasMileage;

CREATE TABLE IF NOT EXISTS gasTable (
    `id` INT NOT NULL AUTO_INCREMENT,
    `Gallons` INT,
    `Mileage` INT,
    `Price` INT,
    `Column_4` VARCHAR(10) CHARACTER SET utf8,
    PRIMARY KEY (id)
);
INSERT INTO gasTable (`Gallons`,`Mileage`,`Price`,`Column_4`) VALUES
    (13.2,350,20.00,NULL),

