SELECT 
    region,
    SUM(amount) AS revenue
FROM orders
WHERE status='shipped'
GROUP BY region
ORDER BY amount DESC
LIMIT 3;