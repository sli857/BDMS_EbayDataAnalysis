SELECT COUNT(DISTINCT C.category)
FROM Categories C JOIN Bids B
ON C.item_id = B.item_id
AND B.amount > 100