-- Task 1: A SQL script that creates a table users with specific attributes.

-- This script checks if the 'users' table exists before attempting to create it,
-- ensuring that the script does not fail if the table already exists.

DROP TABLE IF EXISTS users;
CREATE TABLE `users` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `name` VARCHAR(255),
    `country` ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US',
    PRIMARY KEY (`id`)
);