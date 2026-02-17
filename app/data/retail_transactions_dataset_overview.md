# Retail Transactions Dataset Overview

Last reviewed: 2026-02-15

## Context
This dataset simulates a market basket dataset to help analyze customer purchasing behavior and store operations. It’s useful for market basket analysis, customer segmentation, and general retail analytics.

**Source file:** `data/Retail_Transactions_Dataset.csv`

## Columns
| Column | Description |
| --- | --- |
| `Transaction_ID` | Unique 10-digit identifier for each transaction. |
| `Date` | Timestamp of the purchase. |
| `Customer_Name` | Name of the customer making the purchase. |
| `Product` | List of products purchased (stored as a string representation of a list). |
| `Total_Items` | Total number of items purchased in the transaction. |
| `Total_Cost` | Total cost of the purchase. |
| `Payment_Method` | Payment method used (e.g., credit card, debit card, cash, mobile payment). |
| `City` | City where the purchase took place. |
| `Store_Type` | Store type (e.g., supermarket, convenience store, department store). |
| `Discount_Applied` | Whether a discount was applied (`True`/`False`). |
| `Customer_Category` | Customer background or age group category. |
| `Season` | Season of the purchase (spring, summer, fall, winter). |
| `Promotion` | Promotion type (e.g., None, BOGO, Discount on Selected Items). |

## Sample (first 5 rows)
| Transaction_ID | Date | Customer_Name | Product | Total_Items | Total_Cost | Payment_Method | City | Store_Type | Discount_Applied | Customer_Category | Season | Promotion |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000000000 | 2022-01-21 06:27:29 | Stacey Price | `['Ketchup', 'Shaving Cream', 'Light Bulbs']` | 3 | 71.65 | Mobile Payment | Los Angeles | Warehouse Club | True | Homemaker | Winter | None |
| 1000000001 | 2023-03-01 13:01:21 | Michelle Carlson | `['Ice Cream', 'Milk', 'Olive Oil', 'Bread', 'Potatoes']` | 2 | 25.93 | Cash | San Francisco | Specialty Store | True | Professional | Fall | BOGO (Buy One Get One) |
| 1000000002 | 2024-03-21 15:37:04 | Lisa Graves | `['Spinach']` | 6 | 41.49 | Credit Card | Houston | Department Store | True | Professional | Winter | None |
| 1000000003 | 2020-10-31 09:59:47 | Mrs. Patricia May | `['Tissues', 'Mustard']` | 1 | 39.34 | Mobile Payment | Chicago | Pharmacy | True | Homemaker | Spring | None |
| 1000000004 | 2020-12-10 00:59:59 | Susan Mitchell | `['Dish Soap']` | 10 | 16.42 | Debit Card | Houston | Specialty Store | False | Young Adult | Winter | Discount on Selected Items |

## Common Use Cases
- Market basket analysis (association rules across products)
- Customer segmentation based on purchasing behavior
- Pricing and promotion optimization
- Store and city-level performance trends
- Sales comparison by city (e.g., total revenue and basket size by `City`)
- Store-type analysis (compare `Store_Type` performance across seasons)
- Root cause analysis for sales changes (5 Whys on dips/spikes using `Season`, `Promotion`, `Discount_Applied`, `Payment_Method`)
