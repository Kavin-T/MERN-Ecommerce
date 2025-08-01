# open_close_browser.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def open_browser():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("http://localhost:3000")
    return driver

def main():
    user_input = input("Enter 'open' to open browser and 'close' to close it: ").strip().lower()
    driver = None

    if user_input == "open":
        print("Opening browser...")
        driver = open_browser()
        input("Browser is open. Press Enter to close...")
    else:
        print("Invalid input. Exiting...")

    if driver:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()