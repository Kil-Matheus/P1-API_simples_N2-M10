CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE bloco (
    id SERIAL PRIMARY KEY,
    title TEXT,
    contents TEXT
);

INSERT INTO bloco (title, contents) VALUES ('Teste', 'Valor criar direto do init.sql');