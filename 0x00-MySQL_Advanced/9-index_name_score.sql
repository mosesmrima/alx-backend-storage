-- create an index 'idx_name_first' on table names and the first letter of 'name'
alter TABLE names ADD INDEX idx_name_first_score (name(1), score);
