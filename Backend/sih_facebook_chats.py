import io
import os
import sys
import time
import random
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fpdf import FPDF
from PIL import Image


def random_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))


def login(driver, username, password):
    driver.get("https://www.facebook.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(username)
    driver.find_element(By.NAME, "pass").send_keys(password)
    driver.find_element(By.NAME, "pass").send_keys(Keys.RETURN)
    time.sleep(5)


def navigate_to_messenger(driver):
    driver.get("https://www.facebook.com/messages/t/")
    random_delay(4, 5)  # Random delay after loading the Messenger page

def take_chat_screenshots(driver):
    screenshots = []
    try:
        # Wait for the chat list to load
        chat_list = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Chats']"))
        )
        print("Chat list loaded successfully.")

        # Capture the first chat that automatically opens
        try:
            # Locate the chat message container of the first chat (the one that automatically opens)
            time.sleep(8)
            chat_container = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "(//div[contains(@class, 'x78zum5') and contains(@class, 'xdt5ytf') and contains(@class, 'x1iyjqo2') and contains(@class, 'x6ikm8r') and contains(@class, 'x1odjw0f') and contains(@class, 'xish69e') and contains(@class, 'x16o0dkt')])[2]"))
            )
            print("First chat container loaded successfully.")

            # Check if the chat container is scrollable
            scroll_height = driver.execute_script("return arguments[0].scrollHeight", chat_container)
            client_height = driver.execute_script("return arguments[0].clientHeight", chat_container)

            if scroll_height > client_height:  # Only scroll if the chat has a scrollbar
                chat_container_height = client_height

                while True:
                    # Take a screenshot of the current view of the first chat
                    screenshot_filename = f'chat_screenshot_{len(screenshots) + 1}.png'
                    driver.save_screenshot(screenshot_filename)
                    screenshots.append(screenshot_filename)
                    print(f"Screenshot taken: {screenshot_filename}")

                    # Scroll up by the height of the chat container
                    driver.execute_script("arguments[0].scrollTop -= arguments[1];", chat_container, chat_container_height)
                    random_delay(5, 8)  # Wait for the messages to load

                    # Check if we can still scroll
                    current_scroll_position = driver.execute_script("return arguments[0].scrollTop;", chat_container)
                    if current_scroll_position == 0:  # If we are at the top
                        # Take an additional screenshot at the top before breaking
                        screenshot_filename = f'chat_screenshot_{len(screenshots) + 1}.png'
                        driver.save_screenshot(screenshot_filename)
                        screenshots.append(screenshot_filename)
                        print(f"Screenshot taken at the top: {screenshot_filename}")
                        break
            else:
                # If the chat is not scrollable, take a single screenshot
                screenshot_filename = f'chat_screenshot_{len(screenshots) + 1}.png'
                driver.save_screenshot(screenshot_filename)
                screenshots.append(screenshot_filename)
                print(f"Screenshot taken: {screenshot_filename}")
                
        except TimeoutException:
            print("Failed to locate or capture the first chat.")

        # After capturing the first chat, move on to other chats
        chat_elements = chat_list.find_elements(By.XPATH, "//a[contains(@class, 'x1i10hfl') and contains(@class, 'x1qjc9v5') and contains(@class, 'xjbqb8w') and contains(@class, 'xjqpnuy') and contains(@class, 'xa49m3k') and contains(@class, 'xqeqjp1') and contains(@class, 'x2hbi6w') and contains(@class, 'x13fuv20') and contains(@class, 'xu3j5b3') and contains(@class, 'x1q0q8m5') and contains(@class, 'x26u7qi') and contains(@class, 'x972fbf') and contains(@class, 'xcfux6l') and contains(@class, 'x1qhh985') and contains(@class, 'xm0m39n') and contains(@class, 'x9f619') and contains(@class, 'x1ypdohk') and contains(@class, 'xdl72j9') and contains(@class, 'x2lah0s') and contains(@class, 'xe8uvvx') and contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'x2lwn1j') and contains(@class, 'xeuugli') and contains(@class, 'xexx8yu') and contains(@class, 'x4uap5') and contains(@class, 'x18d9i69') and contains(@class, 'xkhd6sd') and contains(@class, 'x1n2onr6') and contains(@class, 'x16tdsg8') and contains(@class, 'x1hl2dhg') and contains(@class, 'xggy1nq') and contains(@class, 'x1ja2u2z') and contains(@class, 'x1t137rt') and contains(@class, 'x1o1ewxj') and contains(@class, 'x3x9cwd') and contains(@class, 'x1e5q0jg') and contains(@class, 'x13rtm0m') and contains(@class, 'x1q0g3np') and contains(@class, 'x87ps6o') and contains(@class, 'x1lku1pv') and contains(@class, 'x1a2a7pz') and contains(@class, 'x1lliihq')]")
        print(f"Found {len(chat_elements)} other chats.")

        for chat in chat_elements:
            chat.click()  # Open the chat
            random_delay(4, 5)  # Wait for the chat to load
            time.sleep(8)

            # Locate the chat message container
            chat_container = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "(//div[contains(@class, 'x78zum5') and contains(@class, 'xdt5ytf') and contains(@class, 'x1iyjqo2') and contains(@class, 'x6ikm8r') and contains(@class, 'x1odjw0f') and contains(@class, 'xish69e') and contains(@class, 'x16o0dkt')])[2]"))
            )
            print("Chat container loaded successfully.")

            # Check if the chat container is scrollable
            scroll_height = driver.execute_script("return arguments[0].scrollHeight", chat_container)
            client_height = driver.execute_script("return arguments[0].clientHeight", chat_container)

            if scroll_height > client_height:  # Only scroll if the chat has a scrollbar
                chat_container_height = client_height

                while True:
                    # Take a screenshot of the current view
                    screenshot_filename = f'chat_screenshot_{len(screenshots) + 1}.png'
                    driver.save_screenshot(screenshot_filename)
                    screenshots.append(screenshot_filename)
                    print(f"Screenshot taken: {screenshot_filename}")

                    # Scroll up by the height of the chat container
                    driver.execute_script("arguments[0].scrollTop -= arguments[1];", chat_container, chat_container_height)
                    random_delay(5, 8)  # Wait for the messages to load

                    # Check if we can still scroll
                    current_scroll_position = driver.execute_script("return arguments[0].scrollTop;", chat_container)
                    if current_scroll_position == 0:  # If we are at the top
                        # Take an additional screenshot at the top before breaking
                        screenshot_filename = f'chat_screenshot_{len(screenshots) + 1}.png'
                        driver.save_screenshot(screenshot_filename)
                        screenshots.append(screenshot_filename)
                        print(f"Screenshot taken at the top: {screenshot_filename}")
                        break
            else:
                # If the chat is not scrollable, take a single screenshot
                screenshot_filename = f'chat_screenshot_{len(screenshots) + 1}.png'
                driver.save_screenshot(screenshot_filename)
                screenshots.append(screenshot_filename)
                print(f"Screenshot taken: {screenshot_filename}")

    except TimeoutException:
        print("Failed to load the chat list.")
    except NoSuchElementException:
        print("No chat elements found.")

    return screenshots

def generate_pdf(screenshots):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    for screenshot in screenshots:
        img = Image.open(screenshot)
        img_width, img_height = img.size
        scale = min(width / img_width, height / img_height)
        img_width = int(img_width * scale)
        img_height = int(img_height * scale)
        c.drawImage(screenshot, 0, height - img_height, width=img_width, height=img_height)
        c.showPage()

    c.save()
    buffer.seek(0)
    return buffer


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: Missing arguments. Usage: python sih_facebook_chats.py <username> <password>", file=sys.stderr)
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        login(driver, username, password)
        navigate_to_messenger(driver)
        chat_screenshots = take_chat_screenshots(driver)

        if chat_screenshots:
            pdf_buffer = generate_pdf(chat_screenshots)
            sys.stdout.buffer.write(pdf_buffer.getvalue())
        else:
            print("No chat screenshots were taken.", file=sys.stderr)
            sys.exit(1)
    finally:
        driver.quit()