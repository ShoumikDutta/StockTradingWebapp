

## Introduction
This is a Flask web application for managing a finance portfolio. It allows users to register, log in, buy and sell shares of stocks, view their portfolio, and see the transaction history. The application interacts with a SQLite database to store user information, stock data, and transaction history.

## Dependencies
The application requires the following dependencies:
- Flask: A micro web framework for Python.
- Flask-Session: An extension for managing user sessions in Flask.
- SQLite3: A lightweight relational database engine.
- Werkzeug: A comprehensive WSGI web application library.

These dependencies can be installed using pip or any other package manager.

## File Structure
The application consists of the following files:
- `finance.db`: SQLite database file for storing user information, stock data, and transaction history.
- `helpers.py`: Contains helper functions used in the application.
- `templates/`: Directory containing HTML templates used for rendering web pages.
- `application.py`: The main Flask application file containing the routes and logic for the finance application.

## Functionality
### 1. Register
- Route: `/register`
- Methods: GET, POST
- Description: Allows a user to register an account by providing a username and password. The username must be unique. The user's information is stored in the `users` table of the database. A table is also created for the user to store their stock portfolio and transaction history.

### 2. Login
- Route: `/login`
- Methods: GET, POST
- Description: Allows a user to log in to their account by providing their username and password. The user's information is fetched from the `users` table in the database. If the provided username and password match, the user is redirected to the home page. Otherwise, an error message is displayed.

### 3. Logout
- Route: `/logout`
- Description: Clears the user's session and redirects them to the login page.

### 4. Home (Portfolio)
- Route: `/`
- Description: Displays the user's portfolio of stocks. This functionality is not implemented in the provided code (`apology` function is returned instead).

### 5. Buy
- Route: `/buy`
- Methods: GET, POST
- Description: Allows a user to buy shares of a stock. The user can enter the stock symbol and the number of shares to buy. The application fetches the current stock price using the `lookup` function. If the user has enough cash, the transaction is processed and the stock and transaction information are stored in the respective tables in the database. A purchase history table is also created for the user. The user is then redirected to the transaction history page.

### 6. Sell
- Route: `/sell`
- Methods: GET, POST
- Description: Allows a user to sell shares of a stock. This functionality is not implemented in the provided code (`apology` function is returned instead).

### 7. Quote
- Route: `/quote`
- Methods: GET, POST
- Description: Allows a user to get a quote for a stock by entering the stock symbol. The application fetches the current stock information using the `lookup` function and displays it to the user.

### 8. History
- Route: `/history`
- Description: Displays the transaction history of the user. The transaction information is fetched from the respective user's transaction history table in the database.

## Configuration
The application requires some configuration to run properly:
- API_KEY: The API key for accessing stock quotes. It should be set as an environment variable named `API_KEY`.
- Database: The SQLite database file `finance.db` should be present in the same directory as the application file `application.py`.

## Conclusion


This Flask application provides basic functionality for managing a finance portfolio. Users can register, log in, buy and sell shares of stocks, and view their portfolio and transaction history. The application uses SQLite to store user data and interacts with the database to perform various operations.
