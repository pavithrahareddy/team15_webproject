# Library Management System with Flask

This repository contains a Flask-based application that serves as a Library Management System. The system facilitates user authentication, file handling, and MySQL-based CRUD operations for book management. The code employs JWT (JSON Web Tokens) for user authentication, handles file uploads, and enables various book management services.

# Project Demonstration Link
https://drive.google.com/file/d/1Y1OgaxzfaxQvSXMaDA9CbAm63Bbej1nT/view?usp=drive_link

## Application Setup

The Flask application is structured to facilitate Library Management. It integrates with a MySQL database and employs JWT for authentication.

## Setting Up the Application
### To set up and run the application locally, follow these steps:
1) Python: Ensure you have Python installed (preferably Python 3).
2) Dependencies: Install required dependencies using pip install -r requirements.txt.
3) Database Setup: Configure a MySQL database and update the credentials in the application (ie. User name, password, host, DB name, secret key).

## Error Handling

The application includes error handlers for various HTTP status codes to manage different error scenarios effectively. Handlers for 400, 401, 404, 403, and 500 status codes ensure appropriate error messages for the corresponding scenarios.

## Authentication (JWT)

### User Model and Login Endpoint

The code defines a user model with username and password fields. The login endpoint authenticates users and generates a JWT token with a short expiration time upon successful authentication.

### Protected Endpoint

A protected endpoint requires a valid JWT token for access to resources. It validates the token and allows access to protected resources based on the provided credentials.

## File Handling

The application manages file uploads, ensuring that files adhere to specific constraints regarding file type and size. It includes necessary configurations and an endpoint for file upload.

## Public Routes

The public route provides access to a list of predefined classes. It serves as an example of a publicly available endpoint with no authentication requirements.

## Services: MySQL CRUD Operations

The application implements web services to perform Create, Read, Update, and Delete (CRUD) operations in the MySQL database for book management.

### Add, Update, Delete Books

The services include endpoints to add a new book, update an existing book's details, and delete books from the library based on provided parameters.

### Get All Books

The application provides an endpoint to fetch and display all books existing in the library, enabling users to view the entire collection.

## Home Page

The root endpoint serves as a welcome page for the application.

## Usage

To use this application, ensure you have a working MySQL database set up. Run the Flask application using `python project.py` and interact with the specified endpoints to manage users and books.

## Conclusion

This Flask-based Library Management System offers functionalities for user authentication, file handling, and comprehensive book management. It provides a foundational structure for managing a library's book inventory.
