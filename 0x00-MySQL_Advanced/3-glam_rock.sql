-- Task 3: A SQL script that lists all bands with Glam rock as their main style, ranked by their longevity.

-- Column names must be: band_name and lifespan (in year 2022)
-- use attributes formed and split for computing the lifespan.

SELECT band_name, 
       2022 - CAST(formed AS UNSIGNED) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
