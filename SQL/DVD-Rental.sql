/* How many payment transactions were greater than $5.00 */
SELECT COUNT(*) 
FROM payment
WHERE amount > 5.00


/* How many actors have a first name that starts with the letter P */
SELECT COUNT(*) 
FROM actor
WHERE first_name LIKE 'P%'
  

/* How many films begin with the letter 'J' */
SELECT COUNT(title) 
FROM film
WHERE title LIKE 'J%'
  

/* How many unique districts are our customers from? */
SELECT COUNT(DISTINCT(district))
FROM address
ORDER BY district


/* Retrieve the names for those distinct districts */
SELECT DISTINCT(district) 
FROM address


/* How many films have a rating of R and a replacement cost between $5 and $15 */
SELECT title, replacement_cost 
SFROM film
WHERE rating = 'R' AND replacement_cost BETWEEN 5 AND 15


/* How many films have the word Truman somewhere in the title? */
SELECT title FROM film 
WHERE title LIKE '%Truman%'

  
/* Select full names and customer id's of customers having spent more than $100*/
SELECT first_name, last_name, customer.customer_id, SUM(amount) AS total_spent 
FROM customer
JOIN payment 
ON customer.customer_id = payment.customer_id
WHERE store_id = 2
GROUP BY customer.customer_id
HAVING SUM(amount) > 100;


/* Find the customer who has the highest customer id, name starts with an 'E', 
and has an address id lower than 500*/
SELECT first_name, last_name, customer_id 
FROM customer
JOIN address 
ON customer.address_id = address.address_id
WHERE first_name LIKE 'E%' AND address.address_id < 500
ORDER BY customer_id DESC
LIMIT 1
