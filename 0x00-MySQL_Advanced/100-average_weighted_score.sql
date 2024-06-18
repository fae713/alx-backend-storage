-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE weight_score FLOAT;
    SET weight_score = (SELECT SUM(score * weight) / SUM(weight)
                        FROM users AS U
                        JOIN corrections AS C ON U.id=C.user_id
                        JOIN projects AS P ON C.project_id=P.id
                        WHERE U.id=user_id);
    UPDATE users SET average_score = weight_score WHERE id=user_id;
END $$
DELIMITER ;
