import pytest
import os
import random
import time
from utilities import excel_utils
from pages.login_page import LoginPage
from pages.pim_page import PimPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# --- DATA LOADING LOGIC ---
def get_excel_data():
    """
    Reads data from Excel and returns a list of tuples.
    Format: [(user, pass, fname, lname), (user, pass, fname, lname)...]
    """
    # Dynamic path to finding the file
    file_path = os.path.join(os.getcwd(), "test_data", "test_data.xlsx")
    sheet_name = "Sheet1"
    
    data_list = []
    
    # 1. Get total rows
    try:
        rows = excel_utils.get_row_count(file_path, sheet_name)
    except FileNotFoundError:
        print("ERROR: Could not find test_data.xlsx. Make sure the folder and file exist!")
        return []

    # 2. Loop through rows (Start at 2 to skip headers)
    for r in range(2, rows + 1):
        # Column 1=User, 2=Pass, 3=FirstName, 4=LastName
        username = excel_utils.read_data(file_path, sheet_name, r, 1)
        password = excel_utils.read_data(file_path, sheet_name, r, 2)
        fname = excel_utils.read_data(file_path, sheet_name, r, 3)
        lname = excel_utils.read_data(file_path, sheet_name, r, 4)
        
        data_list.append((username, password, fname, lname))
        
    return data_list

# --- TEST CLASS ---

@pytest.mark.usefixtures("driver_setup")
class TestEmployee:

    # Pytest will run this function once for EACH item in the list returned by get_excel_data()
    @pytest.mark.parametrize("username, password, fname, lname", get_excel_data())
    def test_add_employee_ddt(self, username, password, fname, lname):
        driver = self.driver
        login = LoginPage(driver)
        pim = PimPage(driver)
        
        # 1. Login
        # Note: In a real framework, we might check if we are already logged in to save time
        print(f"Logging in as {username}...")
        login.login_to_application(username, password)
        
        # 2. Add Employee
        pim.click_pim_menu()
        pim.click_add_employee()
        
        # 3. Make Data Unique
        # We take the name from Excel but append a random ID so the test doesn't fail on duplicates
        random_id = random.randint(1000, 9999)
        unique_lastname = f"{lname}{random_id}"
        
        print(f"Adding Employee: {fname} {unique_lastname}")
        pim.enter_employee_details(fname, unique_lastname)
        pim.click_save()
        
        # 4. Verify Success
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'oxd-toast-content')]"))
            )
            print("Success message verified!")
            
            # Optional: Write "Passed" back to Excel (Row iteration logic would be needed here)
            # For now, we rely on the HTML report.
            assert True
            
        except:
            print("Failed to add employee.")
            assert False

        # 5. Logout (Cleanup)
        # We must logout so the next iteration (next row in Excel) can log in again.
        # Simple logout logic (Modify locator if needed)
        try:
            driver.find_element(By.CLASS_NAME, "oxd-userdropdown-name").click()
            driver.find_element(By.LINK_TEXT, "Logout").click()
        except:
            pass # If logout fails, the next test might fail or we restart driver