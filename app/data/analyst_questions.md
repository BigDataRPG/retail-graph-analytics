# Data Analyst Questions for Retail Transactions Dataset

These questions are designed to explore the `Retail_Transactions_Dataset.csv` for insights into sales performance, customer behavior, and operational efficiency.

## Overview & Sales Performance
1. What is the total revenue generated across the entire dataset?
2. How has the total revenue trended over the years (2020-2024)?
3. What is the average transaction value (ATV) for the entire period?
4. Which city contributes the highest percentage to the total revenue?
5. How does the average basket size (Total_Items) compare between different Store Types?

## Temporal Analysis (Time & Seasonality)
6. Which season (Spring, Summer, Fall, Winter) generates the highest total sales?
7. Is there a noticeable spike in sales volume during specific months of the year?
8. How does the distribution of transactions vary by time of day (morning, afternoon, evening)?
9. What is the year-over-year growth rate for total transactions?
10. Are there specific days of the week that show consistently higher traffic?

## Customer Segmentation & Behavior
11. Which Customer Category (e.g., Homemaker, Professional, Young Adult) has the highest average spend per transaction?
12. What is the frequency of purchases for the top 10% of customers by revenue?
13. How does the preferred Payment Method vary across different Customer Categories?
14. Do "Young Adult" customers tend to purchase more items per transaction compared to "Retirees"? (assuming Retiree category exists, or general comparison)
15. What is the retention rate of customers year-over-year? (Requires identifying repeat Customer_Names)

## Product & Market Basket Analysis
16. What are the top 5 most frequently purchased products?
17. Which pairs of products are most commonly bought together in the same transaction?
18. What is the average number of distinct products purchased in a single transaction?
19. Which product category seems to be the primary driver for "Warehouse Club" store visits?
20. Are there specific products that are only purchased during specific seasons (e.g., specific seasonal items)?

## Promotions & Discounts
21. What is the conversion rate of transactions with a "BOGO" promotion compared to "Discount on Selected Items"?
22. Does applying a discount (`Discount_Applied = True`) significantly increase the `Total_Items` purchased?
23. What percentage of total transactions involved some form of promotion?
24. Which Store Type utilizes promotions most frequently?
25. Is there a correlation between the magnitude of the "Discount" and the `Total_Cost`?

## Store & Operations
26. Which City has the highest number of unique Store Types represented?
27. How does the `Total_Cost` distribution differ between "Convenience Stores" and "Supermarkets"?
28. What is the preferred payment method in "Los Angeles" versus "New York" (or other cities)?
29. Are "Mobile Payment" methods more common in specific Store Types?
30. Which combination of City and Store Type yields the lowest average transaction value?
