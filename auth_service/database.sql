CREATE DATABASE auth;

CREATE TABLE userlogin(
    id serial PRIMARY KEY, 
    first_name varchar(50),
    last_name varchar(50),
    email varchar(100) UNIQUE NOT NULL,
    contact_no numeric(50) NOT NULL,
    password varchar(250) NOT NULL
)

CREATE TABLE ornamlogin(
    id serial PRIMARY KEY, 
    first_name varchar(50),
    last_name varchar(50),
    email varchar(100) UNIQUE NOT NULL,
    contact_no numeric(50) NOT NULL,
    password varchar(250) NOT NULL
)

    /*database=os.environ.get['DB_NAME']
    user=os.environ.get['DB_USER']
    password=os.environ.get['DB_PASS']
    host=os.environ.get['DB_HOST']
    port=os.environ.get['DB_PORT']*/