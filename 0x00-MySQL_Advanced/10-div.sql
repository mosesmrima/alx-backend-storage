-- Create function that divides 2 numbers and returns result or returns 0 if 2nd param is 0
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT DETERMINISTIC
BEGIN
	IF b = 0 THEN
	   RETURN 0;
	ELSE
	   RETURN (a / b);
	END IF;
END;
$$
