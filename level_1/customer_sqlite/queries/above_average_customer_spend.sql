WITH 
customer_spend AS (
    -- total shipped spend per customer
    SELECT 
        o.customer_id,
        c.name,
        SUM(amount) AS total
    FROM customers c 
    INNER JOIN orders o on c.id =  o.customer_id
    WHERE o.status='shipped'
    GROUP BY o.customer_id, c.name
),
avg_spend AS (
    -- average of customer_spend.total
    SELECT 
        AVG(total) AS avg_total
    FROM customer_spend
)
SELECT cs.name, cs.total
FROM customer_spend cs
CROSS JOIN avg_spend -- creates a cartesian product combination
WHERE cs.total > avg_spend.avg_total
ORDER BY cs.total DESC;