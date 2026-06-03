# Library Management System - Requirements Specification

## Project Overview
This document specifies the requirements for a Flask-based Library Management System web application with SQLite database. The system uses Flask Blueprints for route organization and separates business logic for comprehensive unit testing.

**Total Requirements**: 7 functional requirements (R1-R7).

## Functional Requirements

### R1: Add Book To Catalog
The system shall provide a web interface to add new books to the catalog via a form with the following fields:
- Title (required, max 200 characters)
- Author (required, max 100 characters)
- ISBN (required, exactly 13 digits)
- Total copies (required, positive integer)
- The system shall display success/error messages and redirect to the catalog view after successful addition.

### R2: Book Catalog Display
The system shall display all books in the catalog in a table format showing:
- Book ID, Title, Author, ISBN
- Available copies / Total copies
- Actions (Borrow button for available books)

### R3: Book Borrowing Interface
The system shall provide a borrowing interface to borrow books by patron ID:

- Accepts patron ID and book ID as the form parameters
- Validates patron ID (6-digit format)
- Checks book availability and patron borrowing limits (max 5 books)
- Creates borrowing record and updates available copies
- Displays appropriate success/error messages

### R4: Book Return Processing
The system shall provide a return interface that includes:

- Accepts patron ID and book ID as form parameters
- Verifies the book was borrowed by the patron
- Updates available copies and records return date
- Calculates and displays any late fees owed

### R5: Late Fee Calculation API
The system shall provide an API endpoint GET `/api/late_fee/<patron_id>/<book_id>` that includes the following.
- Calculates late fees for overdue books based on:
  - Books due 14 days after borrowing
  - $0.50/day for first 7 days overdue
  - $1.00/day for each additional day after 7 days
  - Maximum $15.00 per book
- Returns JSON response with fee amount and days overdue

### R6: Book Search Functionality
The system shall provide search functionality with the following parameters:
- `q`: search term
- `type`: search type (title, author, isbn)
- Support partial matching for title/author (case-insensitive)
- Support exact matching for ISBN
- Return results in same format as catalog display

### R7: Patron Status Report 

The system shall display patron status for a particular patron that includes the following: 

- Currently borrowed books with due dates
- Total late fees owed  
- Number of books currently borrowed
- Borrowing history

**Note**: There should be a menu option created for showing the patron status in the main interface

## Non-Functional Requirements
Non-functional requirements (performance, scalability, security) are out of scope for the current version.

## Technical Constraints
- Use Flask with Jinja2 templates for the frontend (already adopted)
- Use SQLite database for data persistence (already adopted)
- Implement modular architecture with Flask 
 Blueprints for route organization (already adopted)
- Separate business logic functions for unit testing (already adopted)
- Book ID must be auto-generated positive integer
- ISBN must be exactly 13 digits
- Library card ID must be exactly 6 digits
- Available copies cannot exceed total copies or be negative
- All monetary values should be displayed with 2 decimal places

## Architecture Requirements
- **Modular Design**: Use Flask Blueprints to organize routes by functionality
- **Separation of Concerns**: Business logic functions must be separate from web routes
- **Testable Structure**: Core functions should be easily unit testable without web context
- **Database Layer**: SQLite operations should be abstracted into dedicated module
- **Application Factory**: Use Flask application factory pattern for better testability

**Note:** The current implementation follows the architectural requirements stated above. Any extension to this project should adopt the same. 
