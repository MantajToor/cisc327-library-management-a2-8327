import pytest
from playwright.sync_api import Page, expect


def test_add_book(page: Page, base_url):

    page.goto(f"{base_url}/add_book")
    
    expect(page.locator("h2")).to_contain_text("Add New Book")
    
    title_textbox = page.get_by_role("textbox", name="Title")
    title_textbox.fill("E2E Test Book")
    
    author_textbox = page.get_by_role("textbox", name="Author")
    author_textbox.fill("Test Author")
    
    isbn_textbox = page.get_by_role("textbox", name="ISBN")
    isbn_textbox.fill("9781234567890")
    
    copies_spinbutton = page.get_by_role("spinbutton", name="Total Copies")
    copies_spinbutton.fill("5")
      
    submit_button = page.get_by_role("button", name="Add Book to Catalog")
    submit_button.click()
    
    success_message = page.get_by_text('Book "E2E Test Book" has been successfully added to the catalog.')
    expect(success_message).to_be_visible()
    
    book_in_table = page.get_by_role("cell", name="E2E Test Book")
    expect(book_in_table).to_be_visible()


def test_borrow_book(page: Page, base_url):

    page.goto(f"{base_url}/catalog")
    expect(page.locator("h2")).to_contain_text("Book Catalog")
    
    book_row = page.get_by_role("row").filter(has_text="The Great Gatsby")
    
    patron_textbox = book_row.get_by_placeholder("Patron ID (6 digits)")
    patron_textbox.fill("123456")

    borrow_button = book_row.get_by_role("button", name="Borrow")
    borrow_button.click()
 
    success_message = page.get_by_text('Successfully borrowed "The Great Gatsby"', exact=False)
    expect(success_message).to_be_visible()
