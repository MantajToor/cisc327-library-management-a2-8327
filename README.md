# Library Management System - Flask Web Application with SQLite

## Overview

This project contains an implementation of a Flask-based Library Management System with SQLite database.

- [`requirements_specification.md`](requirements_specification.md): Complete requirements document with 7 functional requirements (R1-R7)
- [`app.py`](app.py): Main Flask application with application factory pattern
- [`routes/`](routes/): Modular Flask blueprints for different functionalities
  - [`catalog_routes.py`](routes/catalog_routes.py): Book catalog display and management routes
  - [`borrowing_routes.py`](routes/borrowing_routes.py): Book borrowing and return routes
  - [`api_routes.py`](routes/api_routes.py): JSON API endpoints for late fees and search
  - [`search_routes.py`](routes/search_routes.py): Book search functionality routes
- [`database.py`](database.py): Database operations and SQLite functions
- [`library_service.py`](library_service.py): **Business logic functions** (your main testing focus)
- [`templates/`](templates/): HTML templates for the web interface
- [`requirements.txt`](requirements.txt): Python dependencies


## Database Schema
**Books Table:**
- `id` (INTEGER PRIMARY KEY)
- `title` (TEXT NOT NULL)
- `author` (TEXT NOT NULL)  
- `isbn` (TEXT UNIQUE NOT NULL)
- `total_copies` (INTEGER NOT NULL)
- `available_copies` (INTEGER NOT NULL)

**Borrow Records Table:**
- `id` (INTEGER PRIMARY KEY)
- `patron_id` (TEXT NOT NULL)
- `book_id` (INTEGER FOREIGN KEY)
- `borrow_date` (TEXT NOT NULL)
- `due_date` (TEXT NOT NULL)
- `return_date` (TEXT NULL)



