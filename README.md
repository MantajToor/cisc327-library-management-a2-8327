# Library Management System

A Flask web application for managing a library's book catalog, borrowing, and returns. Built with Python, Flask, and SQLite.

## Features

- Browse and search the book catalog (by title, author, or ISBN)
- Add new books with duplicate ISBN detection
- Borrow and return books with availability tracking
- Tiered late fee calculation ($0.50/day for first 7 days, $1.00/day after, capped at $15.00)
- Patron status reports showing currently borrowed books and fees owed
- Payment and refund processing via an injectable payment gateway
- REST API endpoint for late fee lookups (`GET /api/late_fee/<patron_id>/<book_id>`)

## Getting Started

### Prerequisites

- Python 3.9+

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd library-management-system

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
python app.py
```

Visit `http://localhost:5000` in your browser. The database is created automatically on first run and seeded with a few sample books.

## Running Tests

### Unit tests

```bash
pytest tests/ -v
```

### With coverage report

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

### End-to-end tests (requires the app to be running)

```bash
playwright install
pytest tests/e2e/ -v
```

## Project Structure

```
├── app.py                  # Application factory and entry point
├── database.py             # SQLite operations
├── library_service.py      # Core business logic
├── services/
│   ├── library_service.py  # Extended service layer (payment integration)
│   └── payment_service.py  # External payment gateway abstraction
├── routes/
│   ├── catalog_routes.py   # Book catalog and add-book routes
│   ├── borrowing_routes.py # Borrow and return routes
│   ├── search_routes.py    # Search routes
│   └── api_routes.py       # JSON API endpoints
├── templates/              # Jinja2 HTML templates
├── tests/                  # Unit and integration tests
│   └── e2e/                # Playwright end-to-end tests
└── requirements.txt
```

## Database Schema

**books**

| Column | Type |
|---|---|
| `id` | INTEGER PRIMARY KEY |
| `title` | TEXT NOT NULL |
| `author` | TEXT NOT NULL |
| `isbn` | TEXT UNIQUE NOT NULL |
| `total_copies` | INTEGER NOT NULL |
| `available_copies` | INTEGER NOT NULL |

**borrow_records**

| Column | Type |
|---|---|
| `id` | INTEGER PRIMARY KEY |
| `patron_id` | TEXT NOT NULL |
| `book_id` | INTEGER (FK → books) |
| `borrow_date` | TEXT NOT NULL |
| `due_date` | TEXT NOT NULL |
| `return_date` | TEXT (NULL until returned) |
