CREATE DATABASE Ola2;
USE Ola2;


CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50),
    Email VARCHAR(50) UNIQUE,
    password int(20),
    PhoneNumber VARCHAR(15) UNIQUE,
    Address VARCHAR(100)
);

CREATE TABLE Driver (
    DriverID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50),
    Email VARCHAR(50) UNIQUE,
    PhoneNumber VARCHAR(15) UNIQUE,
    Address VARCHAR(100),
    LicenseNo VARCHAR(10) UNIQUE
);


CREATE TABLE Vehicle (
    VehicleID INT AUTO_INCREMENT PRIMARY KEY,
    DriverID INT,
    Model VARCHAR(50),
    License_id VARCHAR(20) UNIQUE,
    Color VARCHAR(20),
    FOREIGN KEY (DriverID) REFERENCES Driver(DriverID)
);
  
  

CREATE TABLE Ride (
    RideID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    DriverID INT,
    PICKUP VARCHAR(100),
    DROP_OFF VARCHAR(100), 
    Distance FLOAT,
    Fare FLOAT,
    RIDEDATE DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (DriverID) REFERENCES Driver(DriverID)
);


CREATE TABLE Payment (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    RideID INT,
    Amount FLOAT,
    PaymentMethod VARCHAR(20),
    PaymentDate DATETIME,
    UPI_ID VARCHAR(50),
    Cash BOOLEAN,  
    Date DATE,
    FOREIGN KEY (RideID) REFERENCES Ride(RideID)
);



CREATE TABLE Feedback (
    FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    RideID INT,
    DriverID INT,
    CustomerID INT,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Comments TEXT,
    FeedbackDate DATETIME,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (DriverID) REFERENCES Driver(DriverID),
    FOREIGN KEY (RideID) REFERENCES Ride(RideID)
);

CREATE TABLE CustomerRide (
    Customer_ID INT,
    Ride_ID INT,
    FOREIGN KEY (Customer_ID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (Ride_ID) REFERENCES Ride(RideID)
);

CREATE TABLE driver_vehicle (
    driver_id INT,
    vehicle_id INT,
    FOREIGN KEY (driver_id) REFERENCES Driver(DriverID),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicle(VehicleID)
);

CREATE TABLE RideFeedback (
    RideID INT,
    FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY (RideID) REFERENCES Ride(RideID),
    FOREIGN KEY (FeedbackID) REFERENCES Feedback(FeedbackID)
);

insert into driver values(101,"Mirno","Mirno12@gmail.com",0645789635,"Jalandhar, Punjab","PB00129423");
insert into driver values(102,"Javed","Javed09@gmail.com",0984235674,"Jalandhar, Punjab","PB00264895");
insert into driver values(103,"Micheal","Mich019@gmail.com",0465123579,"Phagwara, Punjab","PB00065798");
insert into driver values(104,"Ben","Ben491@gmail.com",0817464897,"Jalandhar, Punjab","PB00146025");
insert into driver values(105,"Zeke","Zekel02@gmail.com",0315467895,"Phagwara, Punjab","PB00658792");