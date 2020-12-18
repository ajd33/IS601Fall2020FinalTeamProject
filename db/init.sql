CREATE DATABASE gasMileage;
use gasMileage;

CREATE TABLE IF NOT EXISTS gasTable (
    `id` INT NOT NULL AUTO_INCREMENT,
    `Gallons` INT,
    `Mileage` INT,
    `Price` INT,
    `Column_4` VARCHAR(10) CHARACTER SET utf8,
    `user_id` VARCHAR (20) CHARACTER SET utf8,
    PRIMARY KEY (id)
);
INSERT INTO gasTable (`Gallons`,`Mileage`,`Price`,`Column_4`) VALUES
    (13,350,20,NULL);


create table if not exists gasMileage.users
(
	id int auto_increment,
	first_name varchar(20) null,
	last_name varchar(20) null,
	email varchar(20) null,
	password_hash text null,
	validation_token text null,
	is_admin tinyint(1) null,
	is_verified tinyint(1) null,
	constraint users_id_uindex
		unique (id)
);

alter table gasMileage.users
	add primary key (id);
