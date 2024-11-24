import sys
import time
import os
import io
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from PIL import Image
from reportlab.pdfgen import canvas


def save_screenshots_to_pdf_in_memory(screenshot_paths):
    # Create a PDF in memory with ReportLab
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)

    for screenshot in screenshot_paths:
        image = Image.open(screenshot)
        # Ensure the image is in RGB mode
        image = image.convert("RGB")
        c.setPageSize(image.size)
        c.drawImage(screenshot, 0, 0)
        c.showPage()
    c.save()

    pdf_buffer.seek(0)  # Rewind the buffer to the beginning
    return pdf_buffer


def take_full_page_screenshots(driver, overlap_percentage=0.2):
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    scroll_pause_time = 2  # Pause to allow content to load

    overlap = int(viewport_height * overlap_percentage)
    screenshot_paths = []
    offset = 0
    i = 0

    # Create a directory for temporary screenshots
    temp_dir = "temp_screenshots"
    os.makedirs(temp_dir, exist_ok=True)

    while offset < total_height:
        screenshot_path = os.path.join(temp_dir, f"screenshot_{i + 1}.png")
        driver.save_screenshot(screenshot_path)
        screenshot_paths.append(screenshot_path)

        offset += (viewport_height - overlap)
        driver.execute_script(f"window.scrollTo(0, {offset});")
        time.sleep(scroll_pause_time)

        total_height = driver.execute_script("return document.body.scrollHeight")
        i += 1

        if offset >= total_height:
            break

    return screenshot_paths, temp_dir


# Main function
def main(username, password):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Log in to Facebook
        driver.get('https://www.facebook.com/login')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass"))).send_keys(password + Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.url_contains("facebook.com"))

        time.sleep(5)

        # Navigate to the friend list page
        driver.get("https://www.facebook.com/me/friends")
        time.sleep(5)

        # Take full-page screenshots
        screenshots, temp_dir = take_full_page_screenshots(driver)

        # Save screenshots to an in-memory PDF
        pdf_buffer = save_screenshots_to_pdf_in_memory(screenshots)

        # Clean up temporary screenshots
        for file in screenshots:
            os.remove(file)
        os.rmdir(temp_dir)

        return pdf_buffer

    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        raise

    finally:
        driver.quit()


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    try:
        pdf_buffer = main(username, password)
        sys.stdout.buffer.write(pdf_buffer.getvalue())  # Binary output
    except Exception as e:
        sys.stderr.write(str(e))
