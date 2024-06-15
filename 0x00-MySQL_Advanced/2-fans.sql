-- Task 2: A SQL script that ranks country origins of bands, ordered by the number of (non-unique) fans

-- This script works with metal_bands.sql by creating a column names: origin and nb_fans

SET @row_number = 0;
SET @total_fans = 0;

SELECT origin, (@total_fans := @total_fans + SUM(fans)) AS total_fans, 
       (@row_number := @row_number + 1) AS ranking
FROM metal_bands
GROUP BY origin
ORDER BY total_fans DESC;
