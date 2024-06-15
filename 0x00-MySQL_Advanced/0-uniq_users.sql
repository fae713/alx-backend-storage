-- Task 0: Create a 'users' table with specific attributes

-- This script checks if the 'users' table exists before attempting to create it,
-- ensuring that the script does not fail if the table already exists.

CREATE TABLE IF NOT EXISTS `users` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `name` VARCHAR(255),
    PRIMARY KEY (`id`)
);

