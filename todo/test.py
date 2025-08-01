# Save as test_todo_app_full.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# ---------- Setup ----------
def setup_driver():
    options = Options()
    # options.add_argument('--headless=new')  # Optional: remove to watch it run
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    file_path = os.path.abspath("todo/todo_app.html")
    driver.get("file://" + file_path)
    return driver

# ---------- Helpers ----------
def add_task(driver, task_text):
    input_box = driver.find_element(By.ID, "todoInput")
    input_box.clear()
    input_box.send_keys(task_text)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(0.5)

# ---------- Tests ----------
def test_add_valid_task(driver):
    add_task(driver, "Buy Milk")
    tasks = driver.find_elements(By.TAG_NAME, "li")
    assert any("Buy Milk" in task.text for task in tasks)

def test_add_empty_task(driver):
    add_task(driver, "")
    tasks = driver.find_elements(By.TAG_NAME, "li")
    assert all(task.text != "" for task in tasks)

def test_toggle_done_class(driver):
    add_task(driver, "Task Done Toggle")
    task = driver.find_elements(By.TAG_NAME, "li")[-1]
    task.click()
    assert "done" in task.get_attribute("class")

def test_add_multiple_tasks(driver):
    tasks_text = ["A", "B", "C"]
    for t in tasks_text:
        add_task(driver, t)
    tasks = [task.text for task in driver.find_elements(By.TAG_NAME, "li")]
    for t in tasks_text:
        assert t in tasks

def test_input_cleared_after_add(driver):
    add_task(driver, "Clear Input Test")
    input_box = driver.find_element(By.ID, "todoInput")
    assert input_box.get_attribute("value") == ""

def test_duplicate_tasks(driver):
    add_task(driver, "Duplicate Task")
    add_task(driver, "Duplicate Task")
    tasks = [task.text for task in driver.find_elements(By.TAG_NAME, "li")]
    assert tasks.count("Duplicate Task") == 2

# ---------- Main ----------
if __name__ == "__main__":
    driver = setup_driver()
    try:
        test_add_valid_task(driver)
        test_add_empty_task(driver)
        test_toggle_done_class(driver)
        test_add_multiple_tasks(driver)
        test_input_cleared_after_add(driver)
        test_duplicate_tasks(driver)
        print(" All automated ToDo app tests passed.")
    except AssertionError as e:
        print(" Test failed:", e)
    finally:
        driver.quit()