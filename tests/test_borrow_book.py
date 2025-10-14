import pytest
from library_service import (
    borrow_book_by_patron,
)

"""
### R3: Book Borrowing Interface
The system shall provide a borrowing interface to borrow books by patron ID:
- Accepts patron ID and book ID as the form parameters
- Validates patron ID (6-digit format)
- Checks book availability and patron borrowing limits (max 5 books)
- Creates borrowing record and updates available copies
- Displays appropriate success/error messages
"""

def test_borrow_book_valid_input():
    """Test borrowing a book with valid input."""
    success, message = borrow_book_by_patron("123456", 1)
    
    assert success == True
    assert "Successfully borrowed" in message

def test_borrow_book_invalid_patron_id_too_short():
    """Test borrowing with a patron ID that is too short."""
    success, message = borrow_book_by_patron("12345", 1)
    
    assert success == False
    assert "Invalid patron ID" in message


def test_borrow_book_invalid_patron_id_too_long():
    """Test borrowing with a patron ID too long."""
    success, message = borrow_book_by_patron("1234567", 1)
    
    assert success == False
    assert "Invalid patron ID" in message

def test_borrow_book_invalid_patron_id_non_numeric():
    """Test borrowing with a non-numeric patron ID."""
    success, message = borrow_book_by_patron("12345wrgwrgwra", 1)
    
    assert success == False
    assert "Invalid patron ID" in message

def test_borrow_book_nonexistent_book():
    """Test borrowing a book that doesn't exist."""
    success, message = borrow_book_by_patron("123456", 99999)
    
    assert success == False
    assert "Book not found" in message

