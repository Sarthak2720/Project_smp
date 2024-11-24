import os
import time
import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

# Setting up the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def random_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))

def login_to_telegram(driver):
    driver.get("https://web.telegram.org")
    print("Waiting for Telegram Web to load...")
    try:
        chat_list = WebDriverWait(driver, 600).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='tabs-container']//div[contains(@class, 'scrollable') and contains(@class, 'scrollable-y')]//div[@class='chatlist-top']//ul[@class='chatlist']")
            )
        )
        print("Chat list loaded successfully. Proceeding with the next steps.")
        print("Now waiting for loading all the chats")
        time.sleep(80)  # 1-minute delay
        print("Proceeding to take chat screenshots.")
    except TimeoutException:
        print("Error: Chat list did not load within the expected time.")
        raise

def take_telegram_chat_screenshots(driver):
    screenshots = []
    try:
        # Wait for the chat list to load
        print("Waiting for the chat list to load...")
        chat_list = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='tabs-container']//div[contains(@class, 'scrollable') and contains(@class, 'scrollable-y')]//div[@class='chatlist-top']//ul[@class='chatlist']"))
        )
        print("Chat list loaded successfully.") 
        
        # Get all chat elements
        chat_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'row') and contains(@class, 'no-wrap') and contains(@class, 'row-with-padding') and contains(@class, 'row-clickable') and contains(@class, 'hover-effect') and contains(@class, 'rp') and contains(@class, 'chatlist-chat') and contains(@class, 'chatlist-chat-bigger') and contains(@class, 'row-big')]")
        print(f"Found {len(chat_elements)} chats.")

        for i, chat in enumerate(chat_elements):
            try:
                chat.click()  # Open the chat
                random_delay(2, 4)  # Fixed delay before taking the screenshot

                # Check if the button exists inside the chat container
                try:
                    button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[contains(@class, 'chat-input-container') and contains(@class, 'chat-input-main-container')]//button[contains(@class, 'btn-circle') and contains(@class, 'btn-corner') and contains(@class, 'z-depth-1') and contains(@class, 'bubbles-corner-button') and contains(@class, 'chat-secondary-button') and contains(@class, 'bubbles-go-down') and contains(@class, 'rp') and contains(@class, 'is-broadcast')]")
                        )
                    )
                    print("Button found. Clicking it...")
                    button.click()
                    print("Button clicked. Waiting for 5 seconds.")
                    time.sleep(10)  # Wait 5 seconds after clicking the button
                except TimeoutException:
                    print("Button not found. Proceeding with screenshot capture.")
                    time.sleep(10)  # Wait 5 seconds if button is not found
                    
                # Take a screenshot of the open chat
                screenshot_filename = f'telegram_chat_{i + 1}.png'
                driver.save_screenshot(screenshot_filename)
                screenshots.append(screenshot_filename)
                print(f"Screenshot taken: {screenshot_filename}")

                # Scroll through the chat to capture more content if necessary
                chat_container = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'bubbles') and contains(@class, 'is-chat-input-hidden') and contains(@class, 'has-groups') and contains(@class, 'has-sticky-dates')]//div[contains(@class, 'scrollable') and contains(@class, 'scrollable-y')]"))
                )

                scroll_height = driver.execute_script("return arguments[0].scrollHeight;", chat_container)
                client_height = driver.execute_script("return arguments[0].clientHeight;", chat_container)

                while True:
                    if scroll_height <= client_height:
                        print("No more content to scroll.")
                        break

                    # Take a screenshot while scrolling
                    screenshot_filename = f'telegram_chat_{i + 1}_scroll.png'
                    driver.save_screenshot(screenshot_filename)
                    screenshots.append(screenshot_filename)
                    print(f"Screenshot taken while scrolling: {screenshot_filename}")

                    # Scroll up in the chat
                    driver.execute_script("arguments[0].scrollTop -= arguments[1];", chat_container, client_height)
                    random_delay(2, 4)  # Wait for messages to load

                    # Update scroll height and check if scrolling is complete
                    current_scroll_position = driver.execute_script("return arguments[0].scrollTop;", chat_container)
                    if current_scroll_position == 0:
                        print("Reached the top of the chat.")
                        break

                # Return to the chat list by simulating a click on the back button
                # Go back to the chat list
                driver.back()
                random_delay(2, 4)  # Wait for the chat list to reload

                # Ensure the chat list is visible before moving to the next chat
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='tabs-container']//div[contains(@class, 'scrollable') and contains(@class, 'scrollable-y')]//div[@class='chatlist-top']//ul[@class='chatlist']"))
                )
                print("Back to the chat list. Proceeding to the next chat.")

            except Exception as e:
                print(f"Error with chat {i + 1}: {e}")
                continue  # Move to the next chat even if there's an error with the current one

    except Exception as e:
        print(f"An error occurred: {e}")

    return screenshots

def generate_pdf(screenshots, filename="telegram_chats.pdf"):
    # Save the PDF in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    c = canvas.Canvas(filepath, pagesize=letter)
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
    print(f"PDF saved at: {filepath}")

if __name__ == "__main__":
    try:
        login_to_telegram(driver)
        chat_screenshots = take_telegram_chat_screenshots(driver)
        if chat_screenshots:
            generate_pdf(chat_screenshots, filename="telegram_chats.pdf")
        else:
            print("No chat screenshots were taken.")
    finally:
        driver.quit()
