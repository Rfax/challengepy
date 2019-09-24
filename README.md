# Penn Labs Server Challenge - Penn Clubs API
This document will detail the functions available in the Penn Clubs API, by Lenn Pabs.

## The Data
This API uses a MySQL Database, with the following schema:

```SQL
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
```

A file with the SQL Commands to create the database tables can be found inside the project.

###### Further Improvements:

* In the `pc_clubs` table, more fields could be created (such as `'creator_id'` and `'created_on'`) to keep track of whom created the clubs.


## Features

### Main Page

The main page can be accessed with the url: `'/'`. It simply returns 'Welcome to Penn Club Review'.

### The API
A list of the functions available in this API can be found under `'/api'`

### The INIT function
A `INIT` function has also been provided. This function resets the database and scrapes the data in the "Online Clubs with Penn" deprecated system and inputs it into the database. It also creates the user `jen`, with the password `12345`. The `INIT` function can be called through `'/api/init'`. Of course, on a proper production enviroment this function would never exist. It should be used for testing purposes only.

### Users
#### Login
To use certain API functions (such as adding or removing favorite clubs), users must first identify themselves by sending a `POST` request to the url `'/api/user/login'` passing `JSON` data with the following format:

```JSON
{"username": "user unique identification", "password": "user password" }
```

If they pass a valid username/password combination, they will remain logged into the API until the logout function is called. In the database, passwords are stored as a hash to ensure privacy.


#### Logout
To log out of the API, a user must request `'/api/user/logout'`.


#### Show user
To get user information, one can request `'/api/user/<username>'`. Username must be the unique identification of the user whose information one wants to read. If the user exists, this function will return the username and the user's full name. Both the password and favorite clubs are kept private.

Only a logged user can access this data.

##### Further Improvements:
* A new property in the pc_users table indicating whether a user is enabled.
* A function to create new users. Users allowed to call api methods must be inserted at the pc_users table. This function must receive a unique username, full name and password. All users are initially enabled. 
* A function to disable users. Users should not be completely removed from the system because everything they did must still be traceable back to them. This function will disable the user that is current logged in. After a user is disabled, its username might be used for another user and his favorite clubs are not taken into consideration.
* It is also possible to add an admin property to the pc_users table indicating whether a user is an API administrator. Administrators would have special privileges to call functions such as a disable function that would receive a parameter identifying a user to disable.

### Clubs
#### Creating a Club
To create a new club, send a `POST` request to the url `'/api/clubs'` passing `JSON` data with the following format:

```JSON
{"name": "club name", "description": "club description", "tags": [ "tag1", "tag2" ] }
```

Only a logged user can create a club.

###### Observations:

* Two clubs can have the exact same name, by design.

###### Further Improvements:

* Ability to update and delete clubs
	* Updating the clubs can be easily done by sending in a JSON that also includes the club's ID. The program will recognize this and update instead of inserting a new record into the database.
	* For the delete function, I would create a new url `'/api/clubs/delete/[ID]'`, which recieves the ID, then removes the relative record from the database.
	
#### Accessing the Club Data
To access the club data simply send a get request to `'/api/clubs'`. All of the clubs will be returned on a array in JSON format.

To filter the clubs by either `id`, `name`, or `description`, simply send a url parameter together with the `GET` request. `?id = [id]` will filter by `id`, `?name = [name]` will filter by `name`, and `?desc = [description]` will filter by `description`. The three of them can be sent together or seperately. An example of them being sent together would be:

```URL
/api/clubs?id = [id]&name = [name]&desc = [description]
```

Only a logged user can access the club data.

###### Further Improvements:

* Creating a search function would help those that did not remember the exact name of the club they were searching for. It could be done by sending a filter with a wildcard in each side, and in any spaces they have inside the query.
* It would also be very useful to be able to recieve all the clubs that have a certain tag. With the current data scheme of the API, it can be easily done by joining the `pc_tags_clubs` table with the `pc_clubs` table, then filtering the data with the respective tag id.

### Favorite Clubs
### Adding and removing clubs to your favorites
To add a club to your favorites, be sure to log in, then send a request to `'/api/favorite/add/<club_id>'`, with the `id` of the club you want to favorite.

Similarly, to remove, make sure you are logged in then send a request to `'/api/favorite/remove/<club_id>'`, with the `id` of the club you want to remove.

Because I implemented both add and remove functions, I decided to use `get` instead of `post` for it's practicality and simplicity. It would be simple, however, to implement a `POST` method that would receive a JSON with the operation and its parameters.

### Accessing your favorite clubs
To recieve the information for all your favorite clubs, request `'/api/favorite/'`. The user needs to be logged in to access his favorites.

### Viewing the favorite ranks
To receive the data for all the clubs in order of most popular to least popular, request `'/api/favorite/rankall'`

If you only wish to receive those that have had are favorite to at least 1 person, request `'/api/favorite/rank'`
	
