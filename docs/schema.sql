CREATE DATABASE example;

CREATE TABLE `example`.`tbl_user` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(128) NOT NULL,
  `email` VARCHAR(128) NOT NULL,
  `password` VARCHAR(60) NOT NULL,
  `password_reset_hash` VARCHAR(40),
  `password_reset_exp` DATETIME,
  `registered_on` DATETIME,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
