CREATE DATABASE aitools_ebookwriter;

USE aitools_ebookwriter;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    first_name VARCHAR(50),
    second_name VARCHAR(50),
    role ENUM('admin', 'member') NOT NULL,
    status ENUM('active', 'inactive') NOT NULL
);
