-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN userId INT)
BEGIN
    CREATE TEMPORARY TABLE IF NOT EXISTS temp_avg_score (
        avg_weighted_score DECIMAL(10, 2)
    );
    
    INSERT INTO temp_avg_score (avg_weighted_score)
    SELECT (SUM(score * weight) / SUM(weight))
    FROM scores
    WHERE user_id = userId;
    
    UPDATE users
    INNER JOIN temp_avg_score ON TRUE
    SET users.average_weighted_score = temp_avg_score.avg_weighted_score
    WHERE users.id = userId;
    
    DROP TABLE temp_avg_score;
END$$

DELIMITER ;
