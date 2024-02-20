SELECT COUNT(DISTINCT B.user_id)
FROM Bidders B, Sellers S
WHERE B.user_id = S.user_id