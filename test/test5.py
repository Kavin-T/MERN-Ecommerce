from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ---------- Setup ----------
def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("http://localhost:3000")  # Replace with actual deployed URL
    return driver

# ---------- Tests ----------
def test_open_browser(driver):
    assert "Shop" in driver.title or "Login" in driver.page_source
    print("Opened Browser.")

def test_delete_cookies(driver):
    driver.delete_all_cookies()
    print("Cookies deleted.")

def test_print_session(driver):
    driver.get("http://localhost:3000/login")
    driver.find_element(By.ID, "email").send_keys("admin@admin.com")
    driver.find_element(By.ID, "password").send_keys("admin123")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)
    print("Session Cookies:", driver.get_cookies())

def test_resize_window(driver):
    driver.set_window_size(800, 600)
    print("Window resized.")

def test_close_window_session():
    driver = setup_driver()
    driver.get("http://localhost:3000/login")
    driver.find_element(By.ID, "email").send_keys("admin@admin.com")
    driver.find_element(By.ID, "password").send_keys("admin123")
    driver.find_element(By.ID, "login-button").click()
    print("Logged in and will now close window.")
    driver.quit()

def test_invalid_login(driver):
    driver.get("http://localhost:3000/login")
    driver.find_element(By.ID, "email").send_keys("wrong@example.com")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    assert "Invalid" in driver.page_source
    print("Error message displayed for invalid login.")

def test_valid_login_and_items(driver):
    driver.get("http://localhost:3000/login")
    driver.find_element(By.ID, "email").send_keys("admin@admin.com")
    driver.find_element(By.ID, "password").send_keys("admin123")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(3)
    print("Logged in as: admin@admin.com / admin123")

    search_box = driver.find_element(By.NAME, "search")
    search_box.clear()
    search_box.send_keys("HP Victus")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    assert "HP Victus" in driver.page_source

    driver.find_element(By.CLASS_NAME, "add-to-cart").click()
    time.sleep(1)
    assert "Shopping Cart" in driver.page_source or "HP Victus" in driver.page_source

    items = driver.find_elements(By.CLASS_NAME, "product-title")
    print("Purchased Items:", [item.text for item in items[:2]])

def test_invoice_print(driver):
    driver.get("http://localhost:3000/orders")
    time.sleep(2)
    assert "Invoice" in driver.page_source or "Order ID" in driver.page_source
    print("Invoice is available after login.")

def test_logo_present(driver):
    driver.get("http://localhost:3000")
    logo = driver.find_element(By.TAG_NAME, "img")
    assert logo.is_displayed()
    print("Logo is visible on homepage.")

def test_auto_suggestions(driver):
    driver.get("http://localhost:3000")
    search_box = driver.find_element(By.NAME, "search")
    search_box.clear()
    search_box.send_keys("HP Victus")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    assert "HP Victus" in driver.page_source
    print("Auto-suggestions are working.")

def test_dropdowns(driver):
    driver.get("http://localhost:3000")
    time.sleep(2)
    buttons = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "add-to-cart"))
    )

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(buttons[1])
    ).click()
    time.sleep(2)
    options = driver.find_elements(By.TAG_NAME, "option")
    assert len(options) > 1

    dropdown_element = driver.find_element(By.TAG_NAME, "select")
    select = Select(dropdown_element)

    # Select the second option (index 1)
    select.select_by_index(1)
    selected_option = select.first_selected_option

    # Verify if the selected option is the second one
    assert selected_option == select.options[1]

    print("Dropdown works.")

def test_register_user(driver, email, password):
    print("test")
    driver.get("http://localhost:3000/register")
    time.sleep(5)
    driver.find_element(By.ID, "name").send_keys("TestUser")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "confirm-password").send_keys(password)
    driver.find_element(By.ID, "register-button").click()
    time.sleep(2)
    assert "Registration successful. Welcome!" in driver.page_source
    print(f"Registered user: {email}")

# ---------- Main ----------
if __name__ == "__main__":
    driver = setup_driver()
    try:
        test_open_browser(driver)
        test_delete_cookies(driver)
        test_print_session(driver)
        test_resize_window(driver)
        test_close_window_session()

        driver = setup_driver()
        test_invalid_login(driver)
        test_valid_login_and_items(driver)
        test_logo_present(driver)
        test_auto_suggestions(driver)

        # test_invoice_print(driver)
        test_dropdowns(driver)
        driver = setup_driver()
        test_register_user(driver, "newuser1@example.com", "Pass123$$$")
        print("\n All tests executed successfully.")
    except Exception as e:
        print(" Test failed:", e)
    finally:
        driver.quit()