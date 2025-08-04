from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
import time

USERNAME = "24pa5a0409"
PASSWORD = "phani71805"

def get_attendance():
    # Chrome options
    options = Options()
    # Comment this line if you want to see the browser window
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        # 1. Open the portal
        driver.get("https://vishnu.ac.in/")
        time.sleep(2)

        # 2. Enter login details
        driver.find_element(By.ID, "txtId2").send_keys(USERNAME)
        driver.find_element(By.ID, "txtPwd2").send_keys(PASSWORD)

        # 3. Click the login button
        driver.find_element(By.ID, "imgBtn2").click()
        time.sleep(2)

        # 4. Handle popup alert if it appears
        try:
            alert = Alert(driver)
            print("Popup detected:", alert.text)
            alert.accept()  # Click OK
            time.sleep(2)
        except:
            print("No popup appeared.")

        # 5. Click Attendance in menu
        driver.find_element(By.LINK_TEXT, "Attendance").click()
        time.sleep(2)

        # 6. Click "Till Now"
        driver.find_element(By.LINK_TEXT, "Till Now").click()
        time.sleep(3)

        # 7. Get attendance table text
        attendance_table = driver.find_element(By.TAG_NAME, "table").text
        return attendance_table

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        driver.quit()

if __name__ == "__main__":
    print(get_attendance())
