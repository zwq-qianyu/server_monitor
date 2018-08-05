create database auto;
use auto;

create table users(
	id int unsigned not null AUTO_INCREMENT primary key,
	username varchar(32) not null unique key,
	password varchar(100) not null,
	addtime datetime default null
)AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

create table host(
	id int unsigned not null AUTO_INCREMENT primary key,
	uid int unsigned not null,
	host_user varchar(32) not null,
	host_password varchar(100) not null,
	tag varchar(50),
	ip varchar(32) not null,
	cpu int,
	vir_mem int,
	mem int,
	host_status varchar(50),
	addtime datetime default null
)AUTO_INCREMENT=2;

create table monitor(
	id int unsigned not null AUTO_INCREMENT primary key,
	host_id int unsigned not null,
	cpu_used varchar(32),
	vir_mem_used varchar(32),
	mem_used varchar(32),
	addtime datetime default null,
	time varchar(50) default null
)AUTO_INCREMENT=2;

show databases;
use auto;
show tables;
select * from users;
select * from host;
select * from monitor;
delete from host;
drop database auto;
drop table users;
drop table host;
drop table monitor;
delete from users where username='ziyichen';
