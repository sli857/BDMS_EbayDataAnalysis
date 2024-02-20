SELECT COUNT(users.id) 
FROM (
    SELECT user_id AS id FROM Bidders
    UNION
    SELECT user_id AS id FROM Sellers
) AS users