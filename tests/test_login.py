import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pages.login_page import LoginPage
import time

# This 'fixture' opens the browser before the test and closes it after
@pytest.fixture()
def driver_setup():
    # Automatically downloads and sets up the correct Chrome Driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

# This is your actual test case
def test_valid_login(driver_setup):
    driver = driver_setup
    
    # 1. Initialize the Login Page
    login_page = LoginPage(driver)
    
    # 2. Open the website
    login_page.open_url("https://opensource-demo.orangehrmlive.com/")
    
    # 3. Perform Login (Username: Admin, Password: admin123)
    login_page.login_to_application("Admin", "admin123")
    
    # 4. A small pause to see the result (remove this later)
    time.sleep(5)
    
    # 5. Verify if we are logged in by checking the URL
    assert "dashboard" in driver.current_url