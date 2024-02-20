SELECT COUNT(*)
FROM(
    SELECT C.item_id
    FROM Categories C
    GROUP BY C.item_id
    HAVING COUNT(category) = 4
) AS temp
