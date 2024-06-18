--   a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE avg_weighted_score DECIMAL(10,2);
    
    SELECT AVG(score * weight) INTO avg_weighted_score
    FROM users u
    JOIN corrections c ON u.id = c.user_id
    JOIN projects p ON c.project_id = p.id;
    
    UPDATE users
    SET average_score = avg_weighted_score;
END $$

DELIMITER ;
