## Instructions to install and create a Postgres database on ubuntu

### 1. Update package list
sudo apt update

### 2. Install PostgreSQL and required contrib packages
sudo apt install postgresql postgresql-contrib

### 3. Start PostgreSQL service
sudo systemctl start postgresql

### 4. Check the status of PostgreSQL service
sudo systemctl status postgresql

### 5. Switch to the PostgreSQL user
sudo -i -u postgres

### 6. Access PostgreSQL prompt
psql

### 7. Create a new PostgreSQL user (replace 'your_username' and 'your_password')
CREATE USER your_username WITH PASSWORD 'your_password';

### 8. Grant privileges to the new user
ALTER ROLE your_username CREATEDB;

### 9. Create a new database (replace 'query_results' with your preferred database name)
CREATE DATABASE query_results;

### 10. Connect to the new database
\c query_results

### 11. Create the `queries` table
CREATE TABLE queries (
    id SERIAL PRIMARY KEY,
    query_text TEXT NOT NULL,
    result_text TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

### 12. Create a unique index on `query_text`
CREATE UNIQUE INDEX idx_query_text_unique ON queries(query_text);

### 13. To exit the PostgreSQL prompt
\q

### 14. If you need to connect to the database with the newly created user
psql -U your_username -d query_results
