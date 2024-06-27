CREATE DATABASE ola_app;
USE ola_app;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phoneno int(11) not null
);

CREATE TABLE rides (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pickup VARCHAR(255) NOT NULL,
    dropoff VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE payments(
    id INT AUTO_INCREMENT PRIMARY KEY,
    ride_id INT NOT NULL,
    payment_method VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (ride_id) REFERENCES rides(id)
);

CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ride_id INT NOT NULL,
    rating INT NOT NULL,
    comments TEXT,
    FOREIGN KEY (ride_id) REFERENCES rides(id)
);
