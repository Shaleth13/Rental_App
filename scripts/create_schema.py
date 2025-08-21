import sqlite3

conn = sqlite3.connect("../data/real_estate.db")  
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS Properties (
    property_id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    location TEXT,
    rent INTEGER,
    available INTEGER
);

CREATE TABLE IF NOT EXISTS Bookings (
    booking_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    property_id INTEGER,
    start_date TEXT,
    end_date TEXT,
    FOREIGN KEY(user_id) REFERENCES Users(user_id),
    FOREIGN KEY(property_id) REFERENCES Properties(property_id)
);

CREATE TABLE IF NOT EXISTS Payments (
    payment_id INTEGER PRIMARY KEY,
    booking_id INTEGER,
    amount INTEGER,
    date TEXT,
    FOREIGN KEY(booking_id) REFERENCES Bookings(booking_id)
);
""")
conn.commit()

cursor.executescript("""                               #sample data
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS properties;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS property_photos;
DROP TABLE IF EXISTS favorites;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    role TEXT CHECK(role IN ('landlord','tenant','admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE properties (
    property_id INTEGER PRIMARY KEY AUTOINCREMENT,
    landlord_id INTEGER,
    title TEXT,
    description TEXT,
    property_type TEXT CHECK(property_type IN ('apartment','house','studio','villa')),
    address TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    bedrooms INTEGER,
    bathrooms INTEGER,
    rent_price DECIMAL(12,2),
    status TEXT CHECK(status IN ('available','booked','inactive')),
    listed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (landlord_id) REFERENCES users(user_id)
);

CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER,
    tenant_id INTEGER,
    start_date DATE,
    end_date DATE,
    status TEXT CHECK(status IN ('pending','confirmed','cancelled','completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(property_id),
    FOREIGN KEY (tenant_id) REFERENCES users(user_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    tenant_id INTEGER,
    amount DECIMAL(12,2),
    payment_date DATE,
    status TEXT CHECK(status IN ('initiated','successful','failed','refunded')),
    method TEXT CHECK(method IN ('credit_card','debit_card','bank_transfer','upi','cash')),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
    FOREIGN KEY (tenant_id) REFERENCES users(user_id)
);

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER,
    tenant_id INTEGER,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(property_id),
    FOREIGN KEY (tenant_id) REFERENCES users(user_id)
);

CREATE TABLE property_photos (
    photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER,
    photo_url TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
);

CREATE TABLE favorites (
    tenant_id INTEGER,
    property_id INTEGER,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (tenant_id, property_id),
    FOREIGN KEY (tenant_id) REFERENCES users(user_id),
    FOREIGN KEY (property_id) REFERENCES properties(property_id)
);
""")

cursor.executescript("""
-- Users
INSERT INTO users (first_name,last_name,email,phone,role) VALUES
('Alice','Smith','alice.smith@example.com','1111111111','landlord'),
('Bob','Johnson','bob.johnson@example.com','2222222222','landlord'),
('Charlie','Brown','charlie.brown@example.com','3333333333','tenant'),
('Diana','Miller','diana.miller@example.com','4444444444','tenant'),
('Ethan','Davis','ethan.davis@example.com','5555555555','tenant');

-- Properties
INSERT INTO properties (landlord_id,title,description,property_type,address,city,state,country,bedrooms,bathrooms,rent_price,status) VALUES
(1,'Cozy Apartment','2BHK in central Bradford','apartment','12 High St','Bradford','Yorkshire','UK',2,1,1200,'booked'),
(1,'Family House','Spacious 3BHK with garden','house','45 Green Rd','Bradford','Yorkshire','UK',3,2,1800,'available'),
(2,'Modern Flat','Luxury 2BHK near station','apartment','78 King St','London','London','UK',2,2,2400,'available'),
(2,'Budget Studio','Compact studio for students','studio','89 Queen Rd','London','London','UK',1,1,900,'booked'),
(1,'Villa Retreat','4BHK villa with pool','villa','23 Lakeview','Manchester','Lancashire','UK',4,3,3500,'available');

-- Bookings
INSERT INTO bookings (property_id,tenant_id,start_date,end_date,status) VALUES
(1,3,'2025-01-01','2025-03-31','completed'),
(4,4,'2025-02-01','2025-07-31','confirmed'),
(2, 5, '2025-04-15', '2025-06-15', 'confirmed');

-- Payments
INSERT INTO payments (booking_id,tenant_id,amount,payment_date,status,method) VALUES
(1,3,3600,'2025-03-31','successful','bank_transfer'),
(2,4,5400,'2025-08-01','successful','credit_card');

-- Reviews
INSERT INTO reviews (property_id,tenant_id,rating,comment) VALUES
(1,3,4,'Nice place, comfortable stay'),
(3,4,5,'Excellent flat, very modern'),
(2,5,3,'Decent but a bit noisy');

-- Property Photos
INSERT INTO property_photos (property_id,photo_url) VALUES
(1,'https://example.com/apartment1.jpg'),
(3,'https://example.com/flat1.jpg'),
(5,'https://example.com/villa1.jpg');

-- Favorites
INSERT INTO favorites (tenant_id,property_id) VALUES
(3,2),
(4,3),
(5,1);
""")

conn.commit()
print("Schema + sample data inserted successfully!")
