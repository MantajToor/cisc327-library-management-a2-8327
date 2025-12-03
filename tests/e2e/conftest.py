import pytest
from playwright.sync_api import Page

BASE_URL = "http://localhost:5000"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="function")
def page(page: Page):
    page.set_default_timeout(10000)
    page.set_viewport_size({"width": 1280, "height": 720})
    return page
