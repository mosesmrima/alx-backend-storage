-- creates a trigger that resets the attr 'valid_email' only when the email has been changed
DROP TRIGGER IF EXISTS update_valid_email_attr;
DELIMITER $$
CREATE TRIGGER update_valid_email_attr BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
	if NEW.email != OLD.email THEN
	   SET NEW.valid_email = 0;
	END IF;
END;
$$
