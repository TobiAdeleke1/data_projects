 SELECT 
    c.name,
    c.tier,
    SUM(amount) AS total_spend
FROM customers AS c
INNER JOIN orders AS r
on r.customer_id=c.id
WHERE r.status='shipped'
GROUP BY c.name, c.tier 
ORDER BY  total_spend DESC;