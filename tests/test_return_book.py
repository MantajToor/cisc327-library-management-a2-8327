import pytest
from library_service import (
    return_book_by_patron,
)

"""
### R4: Book Return Processing
The system shall provide a return interface that includes:
- Accepts patron ID and book ID as form parameters
- Verifies the book was borrowed by the patron
- Updates available copies and records return date
- Calculates and displays any late fees owed
"""

def test_return_book_valid_input():
    """Test returning a book with valid input."""
    success, message = return_book_by_patron("123456", 1)
    
    assert success == True
    assert "successfully returned" in message

def test_return_book_invalid_patron_id():
    """Test returning with invalid patron ID."""
    success, message = return_book_by_patron("12345", 1)
    
    assert success == False
    assert "Invalid patron ID" in message

def test_return_book_nonexistent_book():
    """Test returning a book that doesn't exist."""
    success, message = return_book_by_patron("123456", 47232)
    
    assert success == False
    assert "Book not found" in message

def test_return_book_not_borrowed():
    """Test returning a book that wasn't borrowed by this patron."""
    success, message = return_book_by_patron("123456", 2)
    
    assert success == False
    assert "not borrowed" in message
