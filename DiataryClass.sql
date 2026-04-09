-- Used ai to make this part

CREATE DATABASE IF NOT EXISTS FoodReviews;
USE FoodReviews;

CREATE TABLE Diatary_Class (
    DietID INT AUTO_INCREMENT PRIMARY KEY,
    DIET_LABEL VARCHAR(100) NOT NULL
);

INSERT INTO Diatary_Class (DIET_LABEL)
VALUES
    ('None'),
    ('Vegetarian'),
    ('Vegan');