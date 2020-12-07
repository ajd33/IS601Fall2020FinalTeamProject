CREATE DATABASE finalApp;
use finalApp;

create table if not exists finalApp.users
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

alter table finalApp.users
	add primary key (id);
