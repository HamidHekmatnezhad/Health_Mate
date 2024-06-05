CREATE DATABASE IF NOT EXISTS sql_personal_data;

USE sql_personal_data;

CREATE TABLE IF NOT EXISTS personal_data (
    client_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    codeid INT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    face_id VARCHAR(3000),
    birth_date DATE,
    gender VARCHAR(10),
    date_added DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS health_record (
    id_hr INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    hearthbeat SMALLINT,
    oxygen INT,
    weight_kg DECIMAL(5,2),
    temperature DECIMAL(5,2),
    date_added DATETIME NOT NULL,

    FOREIGN KEY (client_id) REFERENCES personal_data(client_id)
);

CREATE TABLE IF NOT EXISTS row_hd (
    r_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    hearthbeat SMALLINT,
    oxygen INT,
    weight_kg DECIMAL(5,2),
    temperature DECIMAL(5,2)
);

CREATE TABLE IF NOT EXISTS control_send (
    f_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    flag BOOLEAN
)