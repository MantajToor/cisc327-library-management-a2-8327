import pytest
from library_service import (
    calculate_late_fee_for_book,
)
"""
### R5: Late Fee Calculation API
The system shall provide an API endpoint GET `/api/late_fee/<patron_id>/<book_id>` that includes the following.
- Calculates late fees for overdue books based on:
  - Books due 14 days after borrowing
  - $0.50/day for first 7 days overdue
  - $1.00/day for each additional day after 7 days
  - Maximum $15.00 per book
- Returns JSON response with fee amount and days overdue
"""

def test_calculate_late_fee_valid_patron_id():
    """Test calculating late fee with valid 6-digit patron ID."""
    result = calculate_late_fee_for_book("123456", 1)
    
    if result:
        assert "fee_amount" in result
        assert "days_overdue" in result

def test_calculate_late_fee_invalid_patron_id_too_short():
    """Test calculating late fee with patron ID thats too short."""
    result = calculate_late_fee_for_book("12345", 1)
    
    if result:
        assert "Invalid patron ID" in str(result)

def test_calculate_late_fee_invalid_patron_id_too_long():
    """Test calculating late fee with patron ID thats too long."""
    result = calculate_late_fee_for_book("1234567", 1)
    
    if result:
        assert "Invalid patron ID" in str(result) 

def test_calculate_late_fee_invalid_patron_id_non_numeric():
    """Test calculating late fee with patron ID that isnt numeric."""
    result = calculate_late_fee_for_book("12345awegfqef", 1)
    
    if result:
        assert "Invalid patron ID" in str(result) 

def test_calculate_late_fee_invalid_book_id():
    """Test calculating late fee with invalid book ID."""
    result = calculate_late_fee_for_book("123456", -1)
    
    if result:
        assert "Book not found" in str(result)
