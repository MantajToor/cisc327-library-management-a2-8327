from unittest import mock
import pytest
from unittest.mock import Mock
from services.library_service import pay_late_fees, refund_late_fee_payment
from services.payment_service import PaymentGateway


def test_pay_late_fees_successful_payment(mocker):

    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 5.50, 'days_overdue': 3}
    )
    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value={'id': 1, 'title': '1984', 'author': 'George Orwell'}
    )

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (
        True,
        "txn_123456_0",
        "Payment of $5.50 processed successfully"
    )

    success, message, transaction_id = pay_late_fees("123456", 1, mock_gateway)

    assert success == True
    assert "Payment successful" in message
    assert transaction_id == "txn_123456_0"

    mock_gateway.process_payment.assert_called_once_with(
        patron_id="123456",
        amount=5.50,
        description="Late fees for '1984'"
    )

def test_pay_late_fee_payment_decline(mocker):

    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 10.00, 'days_overdue': 5}
    )
    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value={'id': 1, 'title': 'Test Book', 'author': 'Test Author'}
    )
        
    mock_gateway = Mock(spec=PaymentGateway)

    mock_gateway.process_payment.return_value = (
        False,
        "",
        "Payment declined: insufficient funds"
    )
        
    success, message, transaction_id = pay_late_fees("123456", 1, mock_gateway)
        
    assert success == False
    assert "Payment failed" in message
    assert "insufficient funds" in message
    assert transaction_id is None
        
    mock_gateway.process_payment.assert_called_once()

def test_pay_late_fee_invalid_patron_id(mocker):

    mock_gateway = Mock(spec=PaymentGateway)

    success, message, transaction_id = pay_late_fees("12345", 1, mock_gateway)

    assert success == False
    assert "Invalid patron ID" in message
    assert "6 digits" in message
    assert transaction_id is None

    mock_gateway.process_payment.assert_not_called()

def test_pay_late_fee_zero_fee(mocker):

    mocker.patch(
    'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 0, 'days_overdue': 0}
    )
    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value={'id': 1, 'title': 'Test Book', 'author': 'Test Author'}
    )

    mock_gateway = Mock(spec=PaymentGateway)

    success, message, transaction_id = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert "No late fees to pay" in message
    assert transaction_id is None

    mock_gateway.process_payment.assert_not_called()
    

def test_pay_late_fee_network_error(mocker):

    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 10, 'days_overdue': 5}
    )
    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value={'id': 1, 'title': 'Test book', 'author': 'Test Author'}
    )
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.side_effect = Exception("timeout")
        
    success, message, transaction_id = pay_late_fees("123456", 1, mock_gateway)
        
    assert success == False
    assert "Payment processing error" in message
    assert "timeout" in message
    assert transaction_id is None

    mock_gateway.process_payment.assert_called_once()


# pay_late_fee tests end here

# refund late fee tests start here


def test_refund_late_fee_payment_success():

    mock_gateway = Mock(spec=PaymentGateway)
    
    mock_gateway.refund_payment.return_value = (
        True, 
        "Refund of $5.50 processed. Refund ID: refund_123456"
    )
    
    success, message = refund_late_fee_payment("txn_123456_0", 5.50, mock_gateway)
    
    assert success == True
    assert "Refund of $5.50 processed" in message
    
    mock_gateway.refund_payment.assert_called_once_with("txn_123456_0", 5.50)


def test_refund_late_fee_payment_invalid_transaction_id():

    mock_gateway = Mock(spec=PaymentGateway)
    
    success, message = refund_late_fee_payment("eafrbawfc", 5.50, mock_gateway)
    
    assert success == False
    assert "Invalid transaction ID" in message
    
    mock_gateway.refund_payment.assert_not_called()

def test_refund_late_fee_payment_negative_amount():

    mock_gateway = Mock(spec=PaymentGateway)
    
    success, message = refund_late_fee_payment("txn_123456_0", -5.00, mock_gateway)
    
    assert success == False
    assert "Refund amount must be greater than 0" in message
    
    mock_gateway.refund_payment.assert_not_called()

def test_refund_late_fee_payment_zero_amount():

    mock_gateway = Mock(spec=PaymentGateway)
    
    success, message = refund_late_fee_payment("txn_123456_0", 0.0, mock_gateway)
    
    assert success == False
    assert "Refund amount must be greater than 0" in message
    
    mock_gateway.refund_payment.assert_not_called()

def test_refund_late_fee_payment_exceeds_maximum():

    mock_gateway = Mock(spec=PaymentGateway)
    
    success, message = refund_late_fee_payment("txn_123456_0", 20.00, mock_gateway)
    
    assert success == False
    assert "Refund amount exceeds maximum late fee" in message
    
    mock_gateway.refund_payment.assert_not_called()

# Any test added past this point is to improve statement coverage

def test_refund_late_fee_gateway_failure(mocker):

    mock_gateway = Mock(spec=PaymentGateway)
    
    mock_gateway.refund_payment.return_value = (
        False, 
        "Transaction already refunded"
    )
    
    success, message = refund_late_fee_payment("txn_123456_0", 5.50, mock_gateway)
    
    assert success == False
    assert "Refund failed" in message
    assert "already refunded" in message
    
    mock_gateway.refund_payment.assert_called_once_with("txn_123456_0", 5.50)

def test_refund_late_fee_gateway_exception(mocker):
 
    mock_gateway = Mock(spec=PaymentGateway)
    
    mock_gateway.refund_payment.side_effect = Exception("Network error")
    
    success, message = refund_late_fee_payment("txn_123456_0", 10.00, mock_gateway)
    
    assert success == False
    assert "Refund processing error" in message
    assert "Network error" in message
    
    mock_gateway.refund_payment.assert_called_once_with("txn_123456_0", 10.00)

def test_pay_late_fee_book_not_found(mocker):
    
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 5.50, 'days_overdue': 3}
    )
    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value=None  # ← Book not found
    )
    
    mock_gateway = Mock(spec=PaymentGateway)
    
    success, message, transaction_id = pay_late_fees("123456", 999, mock_gateway)
    
    assert success == False
    assert "Book not found" in message
    assert transaction_id is None
    
    mock_gateway.process_payment.assert_not_called()

