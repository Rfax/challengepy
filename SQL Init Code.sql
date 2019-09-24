CREATE SCHEMA IF NOT EXISTS pc;

use pc;

DROP TABLE IF EXISTS `pc_user_favorites`;
DROP TABLE IF EXISTS `pc_club_tags`;
DROP TABLE IF EXISTS `pc_tags`;
DROP TABLE IF EXISTS `pc_clubs`;
DROP TABLE IF EXISTS `pc_users`;


CREATE TABLE IF NOT EXISTS `pc_users`(
	`id` bigint (11) unsigned NOT NULL AUTO_INCREMENT,
	`name` varchar (64) NOT NULL,
	`username` varchar (128) NOT NULL,
	`pwd` varchar (256) NOT NULL,
	PRIMARY KEY (`id`)
)	ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `pc_clubs`(
	`id` bigint (11) unsigned NOT NULL AUTO_INCREMENT,
	`name` varchar (128) NOT NULL,
	`description` text NULL,
/*	`creator_id` bigint(11) unsigned NOT NULL,
	`created_on` datetime NOT NULL, */
	PRIMARY KEY (`id`)/*,
	CONSTRAINT `pc_clubs_FKuser` FOREIGN KEY (`creator_id`) REFERENCES `pc_users` (`id`)	*/
)	ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `pc_tags`(
	`id` bigint (11) unsigned NOT NULL AUTO_INCREMENT,
	`tag` varchar (128) NOT NULL,
	PRIMARY KEY (`id`)
)	ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `pc_club_tags`(
	`id` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
	`club_id` bigint(11) unsigned NOT NULL,
	`tag_id` bigint(11) unsigned NOT NULL,
	PRIMARY KEY (`id`),
	CONSTRAINT `pc_clubtags_FKclubs` FOREIGN KEY (`club_id`) REFERENCES `pc_clubs` (`id`),
	CONSTRAINT `pc_clubtags_FKtags` FOREIGN KEY (`tag_id`) REFERENCES `pc_tags` (`id`)	
)	ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `pc_user_favorites`(
	`id` bigint(11) unsigned NOT NULL AUTO_INCREMENT,
	`club_id` bigint(11) unsigned NOT NULL,
	`user_id` bigint(11) unsigned NOT NULL,
	PRIMARY KEY (`id`),
	CONSTRAINT `pc_userfav_FKclubs` FOREIGN KEY (`club_id`) REFERENCES `pc_clubs` (`id`),
	CONSTRAINT `pc_userfav_FKuser` FOREIGN KEY (`user_id`) REFERENCES `pc_users` (`id`)	
)	ENGINE=InnoDB;