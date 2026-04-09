-- Used ai to make this part

CREATE DATABASE IF NOT EXISTS FoodReviews;
USE FoodReviews;

DROP TABLE IF EXISTS Food_Reviews;

CREATE TABLE Food_Reviews (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    FoodName VARCHAR(100) NOT NULL,
    EaseOfMaking DECIMAL(3,1) CHECK (EaseOfMaking >= 0.0 AND EaseOfMaking <= 10.0),
    Taste DECIMAL(3,1) CHECK (Taste >= 0.0 AND Taste <= 10.0),
    DiataryClass INT NOT NULL
);

INSERT INTO Food_Reviews (FoodName, EaseOfMaking, Taste, DiataryClass)
VALUES
    ('Butter chicken', 9.4, 8.6, 1),
    ('Scallion Pancakes', 9.2, 6.3, 3),
    ('Vodka Pasta', 9.6, 9.5, 2),
    ('Thai Red Curry', 9.3, 9.2, 1),
    ('Pad Kra Pao', 9.1, 9.2, 1);