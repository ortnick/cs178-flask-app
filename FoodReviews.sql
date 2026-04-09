-- Used ai to make the setup then edited it a lot

CREATE DATABASE IF NOT EXISTS FoodReviews;
USE FoodReviews;

DROP TABLE IF EXISTS Food_Reviews;
DROP TABLE IF EXISTS Food_Log;

CREATE TABLE Food_Reviews (
    FoodName VARCHAR(100) PRIMARY KEY,
    DietaryClass INT NOT NULL
);

INSERT INTO Food_Reviews (FoodName, DietaryClass)
VALUES
    ('Butter chicken', 1),
    ('Scallion Pancakes', 3),
    ('Vodka Pasta', 2),
    ('Thai Red Curry', 1),
    ('Pad Kra Pao', 1);

    
CREATE TABLE Food_Log (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    FoodName VARCHAR(100) NOT NULL,
    EaseOfMaking DECIMAL(3,1) CHECK (EaseOfMaking >= 0.0 AND EaseOfMaking <= 10.0),
    Taste DECIMAL(3,1) CHECK (Taste >= 0.0 AND Taste <= 10.0)
);

INSERT INTO Food_Log (FoodName, EaseOfMaking, Taste)
VALUES
    ('Butter chicken', 9.4, 8.6),
    ('Butter chicken', 9.2, 8.9),
    ('Scallion Pancakes', 9.2, 6.3),
    ('Vodka Pasta', 9.6, 9.5),
    ('Thai Red Curry', 9.3, 9.2),
    ('Pad Kra Pao', 9.1, 9.2);