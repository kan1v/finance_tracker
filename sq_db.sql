CREATE TABLE IF NOT EXISTS news (
    id integer PRIMARY KEY AUTOINCREMENT,
    news_name text NOT NULL,
    news_text text NOT NULL,
    time integer NOT NULL
);
