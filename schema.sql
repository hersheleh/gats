
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
       post_date string not null,
       author string not null
);

drop table if exists photos;
create table photos (
       id integer primary key autoincrement,
       filename string
);

drop table if exists shows;
create table shows (
       id integer primary key autoincrement,
       show_date string not null,
       venue string not null,	
       city_state not null,
       extra_info,
       link_to_show
);