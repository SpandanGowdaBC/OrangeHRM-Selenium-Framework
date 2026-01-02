import pytest
import os
from datetime import datetime  # <--- This was missing or not copied
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. DRIVER SETUP FIXTURE ---
@pytest.fixture(scope="class")
def driver_setup(request):
    """
    Setup the Chrome driver and pass it to the test class.
    """
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    
    if request.cls is not None:
        request.cls.driver = driver
    
    yield driver
    driver.quit()

# --- 2. SCREENSHOT ON FAILURE LOGIC ---
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            
            # Get driver
            web_driver = None
            if "driver_setup" in item.fixturenames:
                web_driver = item.funcargs['driver_setup']
            
            if web_driver:
                # Create folder if needed
                if not os.path.exists("reports"):
                    os.makedirs("reports")

                # Take screenshot
                timestamp = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
                screenshot_name = f"screenshot_{timestamp}.png"
                screenshot_path = os.path.join("reports", screenshot_name)
                web_driver.save_screenshot(screenshot_path)
                
                # Attach to HTML
                html = f'<div><img src="{screenshot_name}" alt="screenshot" style="width:300px;height:200px;" onclick="window.open(this.src)" align="right"/></div>'
                extra.append(pytest_html.extras.html(html))
        
        report.extra = extra