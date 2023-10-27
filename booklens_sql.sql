-- Begin a transaction block
BEGIN;

-- Delete duplicate entries from the 'books' table, keeping the one with the minimum 'id' for each unique book
DELETE FROM books
WHERE id NOT IN (SELECT MIN(id) FROM books GROUP BY title, author, price, description, rating, num_of_rating, publisher, language, paperback, item_weight, dimensions);

-- Commit the changes made in the transaction block
COMMIT;

-- Delete books with empty author names
DELETE FROM books
WHERE author = '';

-- Count books based on their rating ranges
SELECT
    CASE 
        WHEN rating >= 4.5 THEN '4.5+'
        WHEN rating >= 4.0 THEN '4.0 - 4.4'
        WHEN rating >= 3.5 THEN '3.5 - 3.9'
        ELSE 'Below 3.5'
    END as rating_range,
    COUNT(*) as num_books
FROM books
GROUP BY rating_range;

-- Categorize books into price ranges and count the number of books in each range
SELECT
  price_range,
  COUNT(*) AS num_of_books
FROM (
  SELECT price,
    CASE
      WHEN price BETWEEN 0 AND 29 THEN 'Under $30'
      WHEN price BETWEEN 30 AND 59 THEN '$30-$59'
      WHEN price BETWEEN 60 AND 89 THEN '$60-$89'
      WHEN price BETWEEN 90 AND 119 THEN '$90-$119'
      WHEN price BETWEEN 120 AND 149 THEN '$120-$149'
      WHEN price BETWEEN 150 AND 179 THEN '$150-$179'
      WHEN price BETWEEN 180 AND 209 THEN '$180-$209'
      WHEN price BETWEEN 210 AND 239 THEN '$210-$239'
      WHEN price BETWEEN 240 AND 269 THEN '$240-$269'
      ELSE 'Above 270'
    END AS price_range
  FROM books
) AS grouped_books
GROUP BY price_range
ORDER BY num_of_books DESC;

-- Categorize books into page count ranges and count the number of books in each range
SELECT
  page_range,
  COUNT(*) AS num_of_books
FROM (
  SELECT paperback,
    CASE
      WHEN CAST(paperback AS integer) BETWEEN 100 AND 299 THEN '100-299'
      WHEN CAST(paperback AS integer) BETWEEN 300 AND 499 THEN '300-499'
      WHEN CAST(paperback AS integer) BETWEEN 500 AND 699 THEN '500-699'
      WHEN CAST(paperback AS integer) BETWEEN 700 AND 899 THEN '700-899'
      WHEN CAST(paperback AS integer) BETWEEN 900 AND 1099 THEN '900-1099'
      WHEN CAST(paperback AS integer) BETWEEN 1100 AND 1299 THEN '1100-1299'
      WHEN CAST(paperback AS integer) BETWEEN 1300 AND 1499 THEN '1300-1499'
      ELSE '1500+'
    END AS page_range
  FROM books
) AS grouped_books
GROUP BY page_range
ORDER BY num_of_books DESC;

-- Sum up the number of ratings for each author and display in descending order of total ratings
SELECT author, SUM(num_of_rating) AS total_rating
FROM books
GROUP BY author
ORDER BY total_rating DESC;
