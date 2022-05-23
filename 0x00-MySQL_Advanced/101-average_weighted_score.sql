-- create a stored procedure 'ComputeAverageScoreForUser' to compute and store average score for a student
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
DECLARE user_count INT;
DECLARE u_id INT DEFAULT 1;
DECLARE avg_score FLOAT;
SET user_count = (SELECT count(id) FROM users);

WHILE user_count > 0 DO
      SET avg_score = (SELECT SUM(score * weight) / SUM(weight)
      FROM users as U
      JOIN corrections AS c ON U.id = c.user_id
      JOIN projects AS p ON c.project_id = p.id
      WHERE c.user_id=u_id);
      UPDATE users
      	     SET average_Score = avg_score
      	     WHERE id=u_id;
      SET u_id = u_id + 1;
      SET user_count = user_count - 1;
END WHILE;
END;
$$
