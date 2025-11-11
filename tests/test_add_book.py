import pytest
from services.library_service import (
    add_book_to_catalog,
)
"""
### R1: Add Book To Catalog
The system shall provide a web interface to add new books to the catalog via a form with the following fields:
- Title (required, max 200 characters)
- Author (required, max 100 characters)
- ISBN (required, exactly 13 digits)
- Total copies (required, positive integer)
- The system shall display success/error messages and redirect to the catalog view after successful addition.
"""

def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567899123", 5)
    
    assert success == True
    assert "successfully added" in message

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message

def test_add_book_invalid_isbn_too_long():
    """Test adding a book with ISBN too long."""
    success, message = add_book_to_catalog("Test book", "Test Author", "1234567890123456", 5)

    assert success == False
    assert "13 digits" in message

def test_add_book_invalid_no_author():
    """Test adding a book with no author"""
    success, message = add_book_to_catalog("Test book", "", "1234567890123", 5)

    assert success == False
    assert "Author is required" in message

def test_add_book_invalid_no_title():
    """Test adding a book with no title"""
    success, message = add_book_to_catalog("", "Test Author", "1234567890123", 5)

    assert success == False
    assert "Title is required" in message

def test_add_book_invalid_negative_copies():
    """Test adding a book with negative copies"""
    success, message = add_book_to_catalog("Test book", "Test Author", "1234567890123", -5)

    assert success == False
    assert "Total copies must be a positive integer" in message

def test_add_book_duplicate_isbn():
    
    add_book_to_catalog("Book One", "Author", "1233557890123", 5)
    
    success, message = add_book_to_catalog("Book Two", "Different Author", "1233557890123", 3)
    
    assert success == False
    assert "already exists" in message

def test_add_book_title_too_long():

    title = "A" * 201  
    
    success, message = add_book_to_catalog(title, "Test Author", "1234567890123", 5)
    
    assert success == False
    assert "Title must be less than 200 characters" in message

def test_add_book_author_too_long():

    author = "A" * 101 
    
    success, message = add_book_to_catalog("Test Book", author, "1234567890123", 5)
    
    assert success == False
    assert "Author must be less than 100 characters" in message

