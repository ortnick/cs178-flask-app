CREATE DATABASE IF NOT EXISTS FoodReviews;
USE FoodReviews;

CREATE TABLE Food_Reviews (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    FoodName VARCHAR(100) NOT NULL,
    EaseOfMaking DECIMAL(3,1) CHECK (EaseOfMaking >= 0.0 AND EaseOfMaking <= 10.0),
    Taste DECIMAL(3,1) CHECK (Taste >= 0.0 AND Taste <= 10.0)
);

INSERT INTO Food_Reviews (FoodName, EaseOfMaking, Taste)
VALUES
    ('Butter chicken', 9.4, 8.6),
    ('Scallion Pancakes', 9.2, 6.3),
    ('Vodka Pasta', 9.6, 9.5),
    ('Thai Red Curry', 9.3, 9.2),
    ('Pad Kra Pao', 9.1, 9.2);