-- create a stored procedure 'ComputeAverageScoreForUser' to compute and store average score for a student
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(user_id INT)
BEGIN
DECLARE avg_score FLOAT;
SET avg_score = (SELECT SUM(score * weight) / SUM(weight)
FROM users as U
JOIN corrections AS c ON U.id = c.user_id
JOIN projects AS p ON c.project_id = p.id
WHERE c.user_id=user_id);
UPDATE users
       SET average_Score = avg_score
       WHERE id=user_id;
END;
$$
