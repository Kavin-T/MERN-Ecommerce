from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ---------- Setup ----------
def setup_driver():
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("http://localhost:3000/login")  # Update this URL if hosted elsewhere
    return driver

def clear_login_fields(driver):
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")

    email_field.send_keys(Keys.CONTROL + "a")
    email_field.send_keys(Keys.DELETE)

    password_field.send_keys(Keys.CONTROL + "a")
    password_field.send_keys(Keys.DELETE)

    time.sleep(1)  # optional delay

# ---------- Test Cases ----------
def test_invalid_login(driver):
    driver.find_element(By.ID, "email").send_keys("admin@admin.com")
    driver.find_element(By.ID, "password").send_keys("wrongpassword")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(5)
    assert "Invalid password" in driver.page_source

def test_account_locked(driver):
    clear_login_fields(driver)
    driver.find_element(By.ID, "email").send_keys("admin@admin.com")
    driver.find_element(By.ID, "password").send_keys("wrongpassword")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(5)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(5)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(5)
    assert "Account temporarily locked due to multiple failed login attempts." in driver.page_source

def test_login(driver):
    clear_login_fields(driver)
    driver.find_element(By.ID, "email").send_keys("admin@admin.com")
    driver.find_element(By.ID, "password").send_keys("admin123")
    time.sleep(20)
    driver.find_element(By.ID, "login-button").click()

    WebDriverWait(driver, 20).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Admin User")
    )
    assert "Admin User" in driver.page_source

def test_search_product(driver):
    search_box = driver.find_element(By.NAME, "search")
    search_box.clear()
    search_box.send_keys("HP Victus")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    assert "HP Victus" in driver.page_source

def test_add_to_cart(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "add-to-cart"))
    ).click()
    time.sleep(1)
    assert "Shopping Cart" in driver.page_source or "HP Victus" in driver.page_source

# ---------- Main Execution ----------
if __name__ == "__main__":
    driver = setup_driver()
    try:
        test_invalid_login(driver)
        test_account_locked(driver)
        test_login(driver)
        test_search_product(driver)
        test_add_to_cart(driver)
        print(" All tests passed successfully.")
    except AssertionError as e:
        print(" Test failed:", e)
    finally:
        driver.quit()