CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE bloco (
    title TEXT PRIMARY KEY,
    contents TEXT
);

INSERT INTO bloco VALUES ('Teste', 'Valor criar direto do init.sql');