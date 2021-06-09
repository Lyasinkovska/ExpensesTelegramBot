create table Users
(
    id   integer primary key,
    name varchar(255),
);

create table Expenses
(
    id               integer primary key not null,
    category_id      integer,
    category_name_ua varchar(255),
    user_id          integer,
    amount           float,
    date             datetime_interval_code,
    FOREIGN KEY (category_id) REFERENCES Categories (id),
    FOREIGN KEY (category_name_ua) REFERENCES Categories (name_ua),
    FOREIGN KEY (user_id) REFERENCES Users (id)
);

create table Categories
(
    id      integer primary key,
    name_ua varchar(255)
);

insert into Categories (id, name_ua)
values (0, "Харчування"),
       (1, "Транспорт"),
       (2, "Будинок"),
       (3, "Здоровʼя"),
       (4, "Подарунки"),
       (5, "Послуги"),
       (6, "Одяг"),
       (7, "Інше");