drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    name string not null,
    feeling integer not null
);
