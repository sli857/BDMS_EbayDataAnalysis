drop table if exists Items;
drop table if exists Bids;
drop table if exists Bidders;
drop table if exists Sellers;
drop table if exists Categories;

create table Items(
    item_id INTEGER PRIMARY KEY,
    name CHAR(256),
    currently REAL,
    buy_price REAL,
    first_bid REAL,
    number_of_bids INTEGER,
    location CHAR(128),
    country CHAR(64),
    started CHAR(32),
    ends CHAR(32),
    description CHAR(1024)
);

create table Bids(
    item_id INTEGER,
    user_id CHAR(64),
    time CHAR(32),
    amount REAL,
    PRIMARY KEY (item_id, user_id, time),
    FOREIGN KEY (item_id) REFERENCES Items (item_id),
    FOREIGN KEY (user_id) REFERENCES Bidders (user_id)
);

create table Bidders(
    user_id CHAR(64),
    rating INTEGER,
    location CHAR(128),
    country CHAR(64)
);

create table Sellers(
    item_id INTEGER,
    user_id CHAR(64),
    rating INTEGER,
    location CHAR(128),
    PRIMARY KEY (item_id, user_id),
    FOREIGN KEY (item_id) REFERENCES Items (item_id)
);

create table Categories(
    item_id INTEGER,
    category CHAR(64),
    UNIQUE (item_id, category),
    FOREIGN KEY (item_id) REFERENCES Items (item_id)
);