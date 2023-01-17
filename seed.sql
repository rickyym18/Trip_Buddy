CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(25) UNIQUE NOT NULL,
    password VARCHAR(40) NOT NULL,
    first_name VARCHAR(35),
    last_name VARCHAR(40)
);

CREATE TABLE trips(
    id SERIAL PRIMARY KEY,
    city VARCHAR(35) NOT NULL,
    state VARCHAR(35) NOT NULL,
    category VARCHAR(30) NOT NULL,
    date VARCHAR(20) NOT NULL,
    start_time VARCHAR(20) NOT NULL,
);

CREATE TABLE users_trips(
    user_id INT NOT NULL,
    trip_id INT NOT NULL,
    PRIMARY KEY (user_id, trip_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN key (trip_id) REFERENCES trips(id)
);
