# 🍊 OrangeHRM Automated Testing Framework

## 📌 Project Overview
This project is a robust **Hybrid Automation Framework** designed to test the **OrangeHRM** HR Management System. It leverages the **Page Object Model (POM)** design pattern to ensure code maintainability and **Data-Driven Testing (DDT)** to validate workflows with multiple datasets.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Web Automation:** Selenium WebDriver
* **Testing Framework:** Pytest
* **Data Management:** OpenPyXL (Excel)
* **Reporting:** Pytest-HTML
* **Build Tool:** Pip

## ✨ Key Features
* **Page Object Model (POM):** Clean separation of web elements (Locators) and test logic.
* **Data-Driven Testing:** Automatically reads employee data from Excel (`test_data.xlsx`) and runs tests for each row.
* **Robust Synchronization:** Implements `WebDriverWait` and `ExpectedConditions` to handle dynamic elements (spinners/loaders) without hard-coded sleeps.
* **Automatic Screenshots:** Captures and embeds screenshots in the HTML report whenever a test fails.
* **Centralized Configuration:** Uses `conftest.py` for efficient browser setup and teardown.

## 🚀 How to Run
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/OrangeHRM-Selenium-Framework.git](https://github.com/YOUR_USERNAME/OrangeHRM-Selenium-Framework.git)
    ```
2.  **Install Dependencies:**
    ```bash
    pip install selenium pytest pytest-html openpyxl
    ```
3.  **Run the Test Suite:**
    ```bash
    python -m pytest --html=reports/report.html tests/test_add_employee.py
    ```
4.  **View Report:**
    Open `reports/report.html` in your browser.