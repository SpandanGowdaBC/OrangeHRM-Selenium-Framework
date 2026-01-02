from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PimPage:
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        
        # Locators
        self.menu_pim = (By.XPATH, "//span[text()='PIM']")
        self.add_btn = (By.XPATH, "//button[normalize-space()='Add']")
        self.firstname_input = (By.NAME, "firstName")
        self.lastname_input = (By.NAME, "lastName")
        self.save_btn = (By.XPATH, "//button[@type='submit']")
        
        # Locator for the Spinner/Loader that is blocking clicks
        self.loader = (By.CLASS_NAME, "oxd-form-loader")

    def click_pim_menu(self):
        self.wait.until(EC.element_to_be_clickable(self.menu_pim)).click()

    def click_add_employee(self):
        self.wait.until(EC.element_to_be_clickable(self.add_btn)).click()

    def enter_employee_details(self, fname, lname):
        # 1. Wait for loader to disappear (if any)
        self.wait.until(EC.invisibility_of_element_located(self.loader))
        
        # 2. Wait for field to be visible
        self.wait.until(EC.visibility_of_element_located(self.firstname_input)).send_keys(fname)
        self.driver.find_element(*self.lastname_input).send_keys(lname)

    def click_save(self):
        # CRITICAL FIX: explicit wait for the loader to be INVISIBLE
        self.wait.until(EC.invisibility_of_element_located(self.loader))
        
        # Then wait for the button to be clickable
        self.wait.until(EC.element_to_be_clickable(self.save_btn)).click()