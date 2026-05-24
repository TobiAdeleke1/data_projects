SELECT 
    status,
    SUM(amount) AS revenue,
    COUNT(amount) AS total_orders
FROM orders
GROUP BY status
ORDER BY status DESC;