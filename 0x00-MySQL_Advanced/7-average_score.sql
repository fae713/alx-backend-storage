-- A SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student. Note: An average score can be a decimal

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    -- Directly calculate the average score and update the user's record
    UPDATE users
    SET average_score = COALESCE(AVG(corrections.score), 0)
    WHERE id = user_id AND EXISTS(SELECT 1 FROM corrections WHERE user_id = user_id);
END$$

DELIMITER ;
