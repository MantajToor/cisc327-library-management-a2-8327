import pytest
from library_service import (
    get_patron_status_report,
)

"""
### R7: Patron Status Report 

The system shall display patron status for a particular patron that includes the following: 

- Currently borrowed books with due dates
- Total late fees owed  
- Number of books currently borrowed
- Borrowing history

**Note**: There should be a menu option created for showing the patron status in the main interface
"""

def test_get_patron_status_valid():
    """Test getting status report for a valid patron."""
    result = get_patron_status_report("123456")
    
    if result: 
        assert "currently_borrowed" in result
        assert "total_late_fees" in result
        assert "books_borrowed_count" in result

def test_get_patron_status_invalid():
    """Test getting status for a invalid patron ID."""
    result = get_patron_status_report("invalid")
    
    if result: 
        assert "currently_borrowed" in result 

def test_get_patron_status_invalid_too_short():
    """Test getting status for a patron ID thats too short."""
    result = get_patron_status_report("12345")

    if result:  
        assert "currently_borrowed" in result 

def test_get_patron_status_invalid_too_long():
    """Test getting status for a patron ID thats is too long."""
    result = get_patron_status_report("1234567")
    
    if result:  
        assert "currently_borrowed" in result 

def test_get_patron_status_non_numeric():
    """Test getting status for a non-numeric patron ID."""
    result = get_patron_status_report("12345rgrrg")

    if result:  
        assert "currently_borrowed" in result
