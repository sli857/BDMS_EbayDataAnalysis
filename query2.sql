SELECT COUNT(*) 
FROM (
    SELECT user_id AS id, location AS loc FROM Bidders
    UNION
    SELECT user_id AS id, location AS loc FROM Sellers
) AS users
WHERE loc = "New York"