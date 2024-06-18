-- Write a SQL script that creates an index idx_name_first_score on the table names and the first letter of name and the score.

-- Only the first letter of name AND score must be indexed


ALTER TABLE names
ADD COLUMN name_first CHAR(1) GENERATED ALWAYS AS (SUBSTRING(name, 1, 1)) STORED;
ADD COLUMN score_value DOUBLE GENERATED ALWAYS AS (score) STORED;

CREATE INDEX idx_name_first_score ON names (name_first, score);