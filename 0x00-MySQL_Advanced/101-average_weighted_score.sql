--   a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users AS U
    INNER JOIN (
        SELECT U.id, SUM(C.score * P.weight) / SUM(P.weight) AS w_avg
        FROM users AS U
        JOIN corrections AS C ON U.id = C.user_id
        JOIN projects AS P ON C.project_id = P.id
        GROUP BY U.id
    ) AS WA ON U.id = WA.id
    SET U.average_score = WA.w_avg;
END $$
DELIMITER ;
