# My SQL CheatSheet 

This cheat sheet is designed to help you transition from using Excel or Python to working with **SQL for data manipulation**. If you’re familiar with data handling in other tools, SQL will let you scale that to databases. Here’s a quick guide to essential SQL commands that will optimize your workflow.

Most examples are straightforward and concise, often requiring only one line of code to retrieve and manipulate data from large datasets.

## **Connecting to a Database**

 In Excel, you might import data from a file (e.g., CSV or Excel sheet). In SQL, instead of opening a file, you connect to a database:
 
    CONNECT  TO  'database_name';
## **Selecting Data From Tables**

> Just like selecting a range of cells or specific columns in Excel

**Select all data from a table**

    SELECT * FROM table_name;
 
 **Select specific columns**
 
    SELECT column1, column2 FROM table_name;


## Filtering Data

 > Like Excel's filters, you can filter rows in SQL:

  **Filter rows based on conditions** 
    
    SELECT * FROM table_name
    WHERE column_name = 'some_value';
   
  **Use comparison operators**
   
    SELECT * FROM table_name
    WHERE column_name > 100;
        
 **Using multiple conditions**
 
    SELECT * FROM table_name
    WHERE column1 = 'A' AND column2 = 'B';

## Aggregation and Summarization

> **Basic Aggregation** This is in Excel `SUM()`, `COUNT()`, or `AVERAGE()`, SQL functions are:

  **Count the number of rows (like Excel's COUNTA function)**
  
    SELECT COUNT(*) FROM table_name;
    
  **Sum values in a column (like Excel's SUM function)**
  
    SELECT SUM(column_name) FROM table_name;
    
> **Group By & Having** This is like creating a pivot table in Excel, you group rows by a column and then aggregate:

**Group data and aggregate within groups ( grouping in PivotTables)**

    SELECT column, COUNT(*)
    FROM table_name
    GROUP BY column;

**Filter groups after aggregation (filtering PivotTable results)**

    SELECT column, COUNT(*)
    FROM table_name
    GROUP BY column
    HAVING COUNT(*) > 1;

## Joining Tables

**Inner Join** Similar to doing a `VLOOKUP` or `XLOOKUP` in Excel to bring in matching data from another sheet:

 > Combine rows from two tables where there is a match (like VLOOKUP in Excel)
 
    SELECT a.column, b.column
    FROM table_a a
    INNER JOIN table_b b
    ON a.id = b.id;
    
**Left Join** If you want all the data from one table and only the matching data from the second (just like doing a left join in Excel with `VLOOKUP`):

> Include all rows from the left table (like a VLOOKUP with unmatched rows showing as blanks)

    SELECT a.column, b.column
    FROM table_a a
    LEFT JOIN table_b b
    ON a.id = b.id;


## Data Cleaning

> Select only unique rows (like Excel's "Remove Duplicates")

    SELECT DISTINCT column1, column2
    FROM table_name;
>Filter out NULL values (like filtering out blanks in Excel)

    SELECT * FROM table_name
    WHERE column_name IS NOT NULL;

>Replace NULLs with a default value (like using Excel's IFERROR function to handle blanks)

    SELECT COALESCE(column_name, 'default_value') FROM table_name;

**Update Data** In Excel, you might manually replace values in cells. SQL can automate that across large datasets:

>Update existing values (like using Find and Replace in Excel, but on a massive scale)

    UPDATE table_name
    SET column_name = 'new_value'
    WHERE condition;

## Subqueries and CTEs

### **Subqueries**
 A subquery in SQL is like nesting functions in Excel, where you perform one operation inside another

>Query inside another query (similar to using nested functions in Excel)

    SELECT column_name
    FROM table_name
    WHERE id IN (SELECT id FROM other_table);
#### **Use Case 1**: Filter based on aggregated data

You want to find employees who earn more than the average salary of all employees.

  **Without Subquery**: You’d need to run two separate queries, one to find the average salary, then use that result to filter.

**With Subquery** you can find employees who earn more than the average salary

    SELECT employee_name, salary
    FROM employees
    WHERE salary > (SELECT AVG(salary) FROM employees);

>**Explanation**: The subquery `(SELECT AVG(salary) FROM employees)` calculates the average salary, and then the main query compares each employee’s salary to that result.

#### **Use Case 2**: Filter data from another table

You want to find all customers who have placed an order.
 **With Subquery**: You find customers who have placed an order

    SELECT customer_name
    FROM customers
    WHERE customer_id IN (SELECT customer_id FROM orders);
> **Explanation**: The subquery `(SELECT customer_id FROM orders)` retrieves all customer IDs that exist in the orders table, and the main query uses this list to filter customer

### **Common Table Expressions (CTE)**  
Temporary result sets you can refer to within a SELECT, INSERT, UPDATE, or DELETE query. CTEs are useful when you have complex queries that would otherwise require subqueries. They help make your SQL code more readable and reusable.


    WITH cte_name AS (
       SELECT column_name FROM table_name
    )
    SELECT * FROM cte_name;

#### **Use Case 1**: Break Down Complex Queries

Suppose you need to calculate the total sales per customer, and then you want to find only those customers whose total sales exceed a certain threshold.

 **Without CTE**: You could use a nested subquery, but the query might be hard to read.
 **With CTE**: Find customers with total sales over $5000

    WITH customer_sales AS (
       SELECT customer_id, SUM(order_value) AS total_sales
       FROM orders
       GROUP BY customer_id
    )
    SELECT customer_id, total_sales
    FROM customer_sales
    WHERE total_sales > 5000;
    
> **Explanation**: The CTE  `customer_sales`  calculates the total sales per customer and can be referenced as if it were a temporary table in the main query. This breaks the query into smaller, more understandable parts.

### **Use Case 2**: Recursion and Hierarchical Data

CTEs are especially powerful for recursive queries, like retrieving hierarchical data (e.g., an employee reporting structure).

**With Recursive CTE**: Find all employees reporting to a specific manager

    WITH RECURSIVE EmployeeHierarchy AS (
       SELECT employee_id, manager_id, employee_name
       FROM employees
       WHERE manager_id IS NULL 
       
       UNION ALL
       
       SELECT e.employee_id, e.manager_id, e.employee_name
       FROM employees e
       INNER JOIN EmployeeHierarchy eh ON e.manager_id = eh.employee_id
    )
    SELECT * FROM EmployeeHierarchy;
  
  > **Explanation**: This recursive CTE starts with the top manager and recursively finds all employees who report to that manager, building out the entire organizational hierarchy. Each iteration of the recursion pulls more levels of the reporting structure.
 
## Window Functions

Window functions perform calculations across a set of table rows that are related to the current row, unlike aggregate functions, which return a single value for a set of rows.

> Rank rows within a partition (like using RANK or ROW functions in Excel)

    SELECT column, RANK() OVER (PARTITION BY category ORDER BY score DESC)
    FROM table_name;

> Assign row numbers to rows (like using Excel's ROW function)

    SELECT column, ROW_NUMBER() OVER (ORDER BY column)
    FROM table_name;
    
#### **Use Case 1**: Running Total (Cumulative Sum)

You want to calculate the running total of sales over time for each product.

 **With Window Function**:  Calculate the running total of sales for each product
    
    SELECT product_id, order_date, sales_amount,
           SUM(sales_amount) OVER (PARTITION BY product_id ORDER BY order_date) AS running_total
    FROM sales;
 
> **Explanation**: The  `SUM() OVER (PARTITION BY product_id ORDER BY order_date)`  calculates the running total of sales for each product, similar to how you might calculate a running sum in Excel using a formula across rows.

#### **Use Case 2**: Ranking Data

You want to rank employees based on their sales performance within each department.

 **With Window Function**: Rank employees based on sales within each department

    SELECT employee_id, department_id, sales,
           RANK() OVER (PARTITION BY department_id ORDER BY sales DESC) AS rank
    FROM employee_sales;
    
> **Explanation**:  `RANK() OVER (PARTITION BY department_id ORDER BY sales DESC)`  assigns a rank to each employee within their department based on their sales. This is similar to Excel’s  `RANK()`  function, but more powerful because it works on partitions of the data.

#### **Use Case 3**: Calculating Moving Averages

You need to calculate a 3-month moving average of sales.

  **With Window Function**: Calculate 3-month moving average of sales
 

     SELECT order_date, sales_amount,
               AVG(sales_amount) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg
        FROM sales;
    
> **Explanation**:  `AVG(sales_amount) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`  calculates the moving average over the current row and the previous two rows, similar to how you'd do a moving average calculation in Excel.

## **Performance Optimization**

As datasets grow, SQL queries can slow down. Optimizing performance is critical to ensuring your queries run efficiently.

#### **Use Case 1**: Indexing

Indexes are like creating an index in the back of a book – they allow the database to find data faster. However, indexes can slow down  `INSERT`  and  `UPDATE`  operations because the index must be updated each time data changes.

**Create an Index**: Create an index on a frequently queried column

    CREATE INDEX idx_customer_id ON orders (customer_id);

    
> **Explanation**: This index allows the database to retrieve rows related to a specific  `customer_id`  much faster, improving performance for queries that filter by  `customer_id`. In Excel, this is like sorting a column to make it easier to filter data.
If you're querying the  `customer_id`  column often in the  `orders`  table, indexing that column will improve query performance significantly. 
    

#### **Use Case 2**: Limiting Results

If you’re working with large datasets, limiting the number of rows returned in your query can dramatically improve performance, especially during data exploration.

  **With  `LIMIT`**: Limit the number of rows returned to 100

    SELECT * FROM orders
    LIMIT 100;
    
>**Explanation**: The  `LIMIT`  clause ensures that only 100 rows are returned, which is helpful when you’re just **exploring data** or don’t need the full dataset at once. This is similar to filtering down a portion of a dataset in Excel before running calculations on it.

#### **Use Case 3**: Avoiding  `SELECT *`

Selecting all columns (`SELECT *`) can slow down queries because it retrieves more data than you might need. Instead, specify only the columns you need.

 **Optimized Query**: Avoid SELECT *, only retrieve necessary columns
 
    SELECT customer_id, order_date, total_amount
    FROM orders;
    
 > **Explanation**: By specifying only the columns you need, you reduce the amount of data retrieved and processed, improving query performance. In Excel terms, this narrows your analysis to only a few relevant columns instead of including everything.

#### **Use Case 4**: Query plan analysis ( `EXPLAIN`)

This is to understand how a query is executed. The  `EXPLAIN`  statement shows the execution plan used by the database to retrieve the data.

  **Using  `EXPLAIN`**: Analyze the query
   
     EXPLAIN SELECT customer_id, order_date, total_amount
     FROM orders
     WHERE customer_id = 123; 
    
> **Explanation**:  `EXPLAIN`  helps you understand whether indexes are being used, how many rows are being scanned, and if there are bottlenecks in the query. This is analogous to using a formula evaluator in Excel to see how complex formulas are calculated.

####  **Use Case 5**: Avoiding Unnecessary Joins

Joins can be expensive in terms of query performance, especially if joining large tables. Only join tables when necessary, and use appropriate join types.

  **Optimized Join**: Join only when necessary and use the correct join type

    SELECT o.customer_id, o.order_date, c.customer_name
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id;

 > **Explanation**: An  `INNER JOIN`  is appropriate when you only need matching rows from both tables. Avoid unnecessary joins, just like avoiding unnecessary linked data from multiple Excel sheets to improve calculation speed.
