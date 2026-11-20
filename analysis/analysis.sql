-- 1. Average product price by category
SELECT
    category,
    ROUND(AVG(price), 2) AS avg_price,
    COUNT(*) AS product_count
FROM products_clean
GROUP BY category
ORDER BY avg_price DESC;



-- 2. Average discount percentage by category
SELECT
pc.category,
COUNT(pc.discountPercentage) AS product_count,
ROUND(AVG(pc.discountPercentage),2) AS avg_discount_pct
FROM products_clean pc
GROUP BY pc.category
ORDER BY avg_discount_pct DESC 



-- 3. Products priced below and rated above their category averages
WITH idk AS (
SELECT
pc.category,
AVG(pc.rating) AS avg_rating,
AVG(pc.final_price) AS avg_final_price
FROM products_clean pc 
GROUP BY pc.category 
)
SELECT 
Product_Name,
pc.category,
pc.rating,
i.avg_rating,
pc.final_price,
i.avg_final_price 
FROM products_clean pc JOIN idk i ON pc.category = i.category
WHERE pc.final_price < i.avg_final_price AND pc.rating > i.avg_rating


