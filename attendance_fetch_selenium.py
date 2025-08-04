from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_attendance(username, password):
    options = Options()
    options.add_argument("--headless=new")  # Runs without opening browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://vishnu.ac.in/")
        time.sleep(2)

        # Login with provided credentials
        driver.find_element(By.ID, "txtId2").send_keys(username)
        driver.find_element(By.ID, "txtPwd2").send_keys(password)
        driver.find_element(By.ID, "imgBtn2").click()
        time.sleep(2)

        # Handle login popup
        try:
            alert = Alert(driver)
            alert.accept()
            time.sleep(1)
        except:
            pass

        # Click Attendance link
        attendance_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "ATTENDANCE"))
        )
        attendance_link.click()
        time.sleep(2)

        # Switch to attendance iframe
        driver.switch_to.frame("capIframe")

        # Select "Till Now"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "radTillNow"))
        ).click()
        time.sleep(1)

        # Click Show button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnShow"))
        ).click()
        time.sleep(3)

        # Get table text
        table_text = driver.find_element(By.TAG_NAME, "table").text
        return table_text

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        driver.quit()

# Test run
if __name__ == "__main__":
    id_input = input("Enter Student ID: ")
    pass_input = input("Enter Password: ")
    print(get_attendance(id_input, pass_input))
