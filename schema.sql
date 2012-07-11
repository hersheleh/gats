
create table accounts (
       username string not null,
       password string not null
);


create table news (
       id integer primary key autoincrement,
       rich_text string not null,
       filename string
);

create table photos (
       id integer primary key autoincrement,
       filename string
);