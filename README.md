# Stori Challenge

This project processes transaction data from a CSV file, sends a summary email, and saves the processed data to a database. The project can be run locally or via Docker.

**You can run the project via Docker.**

First, copy the .env.example file to a new file named .env:
`cp .env.example .env`

Then, update the .env file with the necessary values.

To build and run the project with Docker Compose, run the following command:
`docker-compose up --build`

The data that will be processed is in this following path: src/data. The data is in a CSV file named `transactions.csv`.

We use mysql for the database.
We also use the following libraries:
- alembic: for database migrations
- sqlalchemy: for the ORM
- pandas: for data processing
