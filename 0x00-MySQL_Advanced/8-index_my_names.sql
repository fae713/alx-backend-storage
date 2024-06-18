-- a SQL script that creates an index idx_name_first on the table names and the first letter of name.

-- It imports a table dumb: names.sql and index only the first letter. 

CREATE INDEX idx_name_first ON names(name(1));
