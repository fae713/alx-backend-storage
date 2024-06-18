-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score DECIMAL(10, 2) DEFAULT 0;
    DECLARE total_weight DECIMAL(10, 2) DEFAULT 0;
    DECLARE weighted_average DECIMAL(10, 2);
    
    -- Calculate the total weighted score and total weight for the user
    SELECT SUM(s.score * w.weight) INTO total_score
    FROM scores s
    JOIN weights w ON s.type_id = w.type_id
    WHERE s.user_id = user_id;

    SELECT SUM(w.weight) INTO total_weight
    FROM scores s
    JOIN weights w ON s.type_id = w.type_id
    WHERE s.user_id = user_id;
    
    -- Compute the weighted average
    IF total_weight > 0 THEN
        SET weighted_average = total_score / total_weight;
    ELSE
        SET weighted_average = 0;
    END IF;
    
    -- Insert or update the average weighted score in the user_scores table
    INSERT INTO user_scores (user_id, weighted_average)
    VALUES (user_id, weighted_average)
    ON DUPLICATE KEY UPDATE weighted_average = VALUES(weighted_average);
END //

DELIMITER ;
