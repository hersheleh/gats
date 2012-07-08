drop table if exists accounts;
create table accounts (
       username string not null,
       password string not null
);

drop table if exists news;
create table news (
       id integer primary key autoincrement,
       rich_text string not null,
       filename string
);