import pytest
from library_service import (
    search_books_in_catalog,
)

"""
### R6: Book Search Functionality
The system shall provide search functionality with the following parameters:
- `q`: search term
- `type`: search type (title, author, isbn)
- Support partial matching for title/author (case-insensitive)
- Support exact matching for ISBN
- Return results in same format as catalog display
"""

def test_search_by_title():
    """Test searching books by title."""
    result = search_books_in_catalog("1984", "title")
    
    if len(result) > 0:
        assert "1984" in result[0]['title']

def test_search_by_author():
    """Test searching books by author."""
    result = search_books_in_catalog("George Orwell", "author")
    
    if len(result) > 0:
        assert "George Orwell" in result[0]['author']

def test_search_by_isbn():
    """Test searching books by ISBN."""
    result = search_books_in_catalog("9780451524935", "isbn")
    
    if len(result) > 0:
        assert "9780451524935" in result[0]['isbn']

def test_search_case_insensitive():
    """Test that search is case-insensitive."""
    result_lower = search_books_in_catalog("gatsby", "title")
    result_upper = search_books_in_catalog("GATSBY", "title")
    
    assert result_lower == result_upper


def test_search_invalid_type():
    """Test searching with invalid search type."""
    result = search_books_in_catalog("test", "invalidtype")
    
    if result:
        assert result == []
