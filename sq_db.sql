CREATE TABLE IF NOT EXISTS news (
    id integer PRIMARY KEY AUTOINCREMENT,
    news_name text NOT NULL,
    news_text text NOT NULL,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    email text NOT NULL,
    hash_password text NOT NULL
);
