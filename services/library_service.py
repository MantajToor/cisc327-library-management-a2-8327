"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books,get_patron_borrowed_books
)
from services.payment_service import PaymentGateway

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed > 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.

    TODO: Implement R4 as per requirements
    """

    # Check valid patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."

    # Check Valid Book ID
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."

    # Check borrow record 
    borrowed_books = get_patron_borrowed_books(patron_id)
    
    # Check if the book is borrowed by the patron
    borrowed_book = None
    for borrowed in borrowed_books:
        if borrowed['book_id'] == book_id:
            borrowed_book = borrowed
            break
    
    if not borrowed_book:
        return False, "This book was not borrowed by this patron"

    # Record the return date of the book
    return_date = datetime.now()

    return_success = update_borrow_record_return_date(patron_id, book_id, return_date)
    if not return_success:
        return False, "error occurred while recording return date."

    # Increase the amount of books available by 1
    availability_success = update_book_availability(book_id, 1)
    if not availability_success:
        return False, "error occurred while updating book availability."

    # Calculate and display late fees if applicable
    late_fee_info = calculate_late_fee_for_book(patron_id, book_id)
    late_fee_message = ""
    if late_fee_info and late_fee_info.get('late_fee', 0) > 0:
        late_fee_message = f" Late fee: ${late_fee_info['late_fee']}"

    return True, f'Book "{book["title"]}" successfully returned.{late_fee_message}'

def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    
    TODO: Implement R5 as per requirements 
    
    The system shall provide an API endpoint GET `/api/late_fee/<patron_id>/<book_id>` that includes the following.
- Calculates late fees for overdue books based on:
  - Books due 14 days after borrowing
  - $0.50/day for first 7 days overdue
  - $1.00/day for each additional day after 7 days
  - Maximum $15.00 per book
- Returns JSON response with fee amount and days overdue
    

@api_bp.route('/late_fee/<patron_id>/<int:book_id>')
def get_late_fee(patron_id, book_id):
    
    -Calculate late fee for a specific book borrowed by a patron.
    -API endpoint for R4: Late Fee Calculation
    
    result = calculate_late_fee_for_book(patron_id, book_id)
    return jsonify(result), 501 if 'not implemented' in result.get('status', '') else 200


    return { // return the calculated values
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Late fee calculation not implemented'
    }
    """

    # Check valid patron id
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."

    # Check valid book id
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."


    # Check patron's current borrowed books
    current_borrowed = get_patron_borrowed_books(patron_id)

    # Check borrow and return/current date
    for item in current_borrowed:
        if item['book_id'] == book_id:
            due = item['due_date']
            current = datetime.now()
            
            # Calculating days overdue
            if current > due:
                days_overdue = (current - due).days
            else:
                days_overdue = 0
            
            # Calculating late fee
            fee_amount = 0.0
            if (days_overdue > 0 and days_overdue <= 7):
                fee_amount = days_overdue * 0.5
            elif (days_overdue > 7 and days_overdue < 19):
                temp = days_overdue - 7 
                fee_amount = (temp * 1) + 3.5
            elif (days_overdue > 19):
                fee_amount = 15
                
            
            return {
                'fee_amount': fee_amount,
                'days_overdue': days_overdue,
                'status': 'success'
            }
    
    # Book not found
    return {
        'fee_amount': 0.0,
        'days_overdue': 0,
        'status': 'Book was not borrowed by patron'
    }

def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """w
    Search for books in the catalog.
    The system shall provide search functionality with the following parameters:
- `q`: search term
- `type`: search type (title, author, isbn)
- Support partial matching for title/author (case-insensitive)
- Support exact matching for ISBN
- Return results in same format as catalog display

    TODO: Implement R6 as per requirements
    """

    results = []

    # Get book by title
    if search_type.lower() == "title":
        book_title = get_all_books()
        for book in book_title:
            if search_term.lower() in book['title'].lower():
                results.append(book)

    # Get book by author
    elif search_type.lower() == "author":
        all_books = get_all_books()
        for book in all_books:
            if search_term.lower() in book['author'].lower():
                results.append(book)

    # Get book by isbn
    elif search_type.lower() == "isbn":
        book_isbn = get_book_by_isbn(search_term)
        if book_isbn: 
            results.append(book_isbn)
    
    return results

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    
    ### R7: Patron Status Report 

The system shall display patron status for a particular patron that includes the following: 

- Currently borrowed books with due dates
- Total late fees owed  
- Number of books currently borrowed
- Borrowing history

**Note**: There should be a menu option created for showing the patron status in the main interface

    TODO: Implement R7 as per requirements
    """

    # Check patrons current borrowed books
    current_borrowed = get_patron_borrowed_books(patron_id)

    # Due dates of borrowed books
    book_titles = []
    due_dates = []
    for item in current_borrowed:
        book_titles.append(item['title'])
        due_dates.append(item['due_date'])

    # Check total late fees owed
    total_late_fees = 0.0
    for book in current_borrowed:
        late_fee_info = calculate_late_fee_for_book(patron_id, book['book_id'])
        if late_fee_info and late_fee_info.get('late_fee', 0) > 0:
            total_late_fees += late_fee_info['late_fee']

    # Number of books currently borrowed
    books_borrowed_count = get_patron_borrow_count(patron_id)

    return {
        'patron_id': patron_id,
        'currently_borrowed': current_borrowed,
        'book_titles': book_titles,
        'due_dates': due_dates,
        'total_late_fees': total_late_fees,
        'books_borrowed_count': books_borrowed_count,
    }

def pay_late_fees(patron_id: str, book_id: int, payment_gateway: PaymentGateway = None) -> Tuple[bool, str, Optional[str]]:
    """
    Process payment for late fees using external payment gateway.
    
    NEW FEATURE FOR ASSIGNMENT 3: Demonstrates need for mocking/stubbing
    This function depends on an external payment service that should be mocked in tests.
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book with late fees
        payment_gateway: Payment gateway instance (injectable for testing)
        
    Returns:
        tuple: (success: bool, message: str, transaction_id: Optional[str])
        
    Example for you to mock:
        # In tests, mock the payment gateway:
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
        success, msg, txn = pay_late_fees("123456", 1, mock_gateway)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits.", None
    
    # Calculate late fee first
    fee_info = calculate_late_fee_for_book(patron_id, book_id)
    
    # Check if there's a fee to pay
    if not fee_info or 'fee_amount' not in fee_info:
        return False, "Unable to calculate late fees.", None
    
    fee_amount = fee_info.get('fee_amount', 0.0)
    
    if fee_amount <= 0:
        return False, "No late fees to pay for this book.", None
    
    # Get book details for payment description
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found.", None
    
    # Use provided gateway or create new one
    if payment_gateway is None:
        payment_gateway = PaymentGateway()
    
    # Process payment through external gateway
    # THIS IS WHAT YOU SHOULD MOCK IN THEIR TESTS!
    try:
        success, transaction_id, message = payment_gateway.process_payment(
            patron_id=patron_id,
            amount=fee_amount,
            description=f"Late fees for '{book['title']}'"
        )
        
        if success:
            return True, f"Payment successful! {message}", transaction_id
        else:
            return False, f"Payment failed: {message}", None
            
    except Exception as e:
        # Handle payment gateway errors
        return False, f"Payment processing error: {str(e)}", None


def refund_late_fee_payment(transaction_id: str, amount: float, payment_gateway: PaymentGateway = None) -> Tuple[bool, str]:
    """
    Refund a late fee payment (e.g., if book was returned on time but fees were charged in error).
    
    NEW FEATURE FOR ASSIGNMENT 3: Another function requiring mocking
    
    Args:
        transaction_id: Original transaction ID to refund
        amount: Amount to refund
        payment_gateway: Payment gateway instance (injectable for testing)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate inputs
    if not transaction_id or not transaction_id.startswith("txn_"):
        return False, "Invalid transaction ID."
    
    if amount <= 0:
        return False, "Refund amount must be greater than 0."
    
    if amount > 15.00:  # Maximum late fee per book
        return False, "Refund amount exceeds maximum late fee."
    
    # Use provided gateway or create new one
    if payment_gateway is None:
        payment_gateway = PaymentGateway()
    
    # Process refund through external gateway
    # THIS IS WHAT YOU SHOULD MOCK IN YOUR TESTS!
    try:
        success, message = payment_gateway.refund_payment(transaction_id, amount)
        
        if success:
            return True, message
        else:
            return False, f"Refund failed: {message}"
            
    except Exception as e:
        return False, f"Refund processing error: {str(e)}"