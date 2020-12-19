CREATE DATABASE gasMileage;
use gasMileage;

CREATE TABLE IF NOT EXISTS gasTable (
    `id` INT NOT NULL AUTO_INCREMENT,
    `Gallons` INT,
    `Miles` INT,
    `Price` INT,
    `Mileage` FLOAT(11,2),
    `user_id` VARCHAR (20) CHARACTER SET utf8,
    PRIMARY KEY (id)
);

INSERT INTO gasTable (Gallons, Miles, Price, Mileage, user_id) VALUES (5, 12, 12, 10000, 1);

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

INSERT INTO users (first_name, last_name, email, is_admin, is_verified, password_hash)
VALUES ('Joe', 'Smoe', 'joe_smoe@email.com', 1, 1, 'pbkdf2:sha256:150000$DaMT2glz$178030158244b6661eca2f85540d060f3091bdc99bad89487c7eadc6ad69fae2');

alter table gasMileage.users
	add primary key (id);
