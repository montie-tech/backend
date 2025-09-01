CREATE DATABASE recipe_db;
USE recipe_db;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL
);

-- Recipes table
CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(255) NOT NULL,
    ingredients TEXT,
    instructions TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
