CREATE DATABASE IF NOT EXISTS `db_livros`;
USE `db_livros`;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recomendacoes (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL, 
);

CREATE TABLE IF NOT EXISTS favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    livro TEXT NOT NULL,
    escritor TEXT NOT NULL
);
