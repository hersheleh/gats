
create table if not exists accounts (
       username string not null,
       password string not null
);

drop table if exists news;
create table news (
       id integer primary key autoincrement,	
       title string not null, 
       rich_text string not null,
       filename string,
       post_date string not null
);

drop table if exists photos;
create table photos (
       id integer primary key autoincrement,
       filename string
);