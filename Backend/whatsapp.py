import time
import os
import random
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image

# Setting up the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def random_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))

def login_to_whatsapp(driver):
        driver.get("https://web.whatsapp.com")
        
        # Wait for the QR code to be scanned and the chat list to load
        print("Waiting for QR code scan...")
        WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Chat list' and @role='grid']"))
        )
        print("Chat list loaded successfully. Proceeding with the next steps.")
    
        try:
            # Click the settings button
            print("Attempting to find and click the settings button for syncing.")
            settings_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Settings' and @role='button' and contains(@class, '_ajv6') and contains(@class, 'x1y1aw1k') and contains(@class, 'x1sxyh0') and contains(@class, 'xwib8y2') and contains(@class, 'xurb0ha')]"))
            )
            settings_button.click()
            print("Clicked the settings button.")
    
            # Click the sync button
            sync_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'x1c4vz4f') and contains(@class, 'xs83m0k') "
                   "and contains(@class, 'xdl72j9') and contains(@class, 'x1g77sc7') "
                   "and contains(@class, 'x78zum5') and contains(@class, 'xozqiw3') "
                   "and contains(@class, 'x1oa3qoh') and contains(@class, 'x12fk4p8') "
                   "and contains(@class, 'xexx8yu') and contains(@class, 'x4uap5') "
                   "and contains(@class, 'x18d9i69') and contains(@class, 'xkhd6sd') "
                   "and contains(@class, 'xeuugli') and contains(@class, 'x2lwn1j') "
                   "and contains(@class, 'x1nhvcw1') and contains(@class, 'xdt5ytf') "
                   "and contains(@class, 'x1qjc9v5')]//button[2]"))
        )
            sync_button.click()
            print("Clicked the sync button in settings.")
    
            # Wait for the progress bar to reach 100
            print("Waiting for the progress bar to reach 100%...")
            WebDriverWait(driver, 240).until(
                lambda d: d.find_element(By.XPATH, "//progress[@class='_ak0k']").get_attribute("value") == "100"
            )
            print("Progress bar reached 100%.")
    
            # Click the OK button
            ok_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'x889kno') and contains(@class, 'x1a8lsjc') and contains(@class, 'xbbxn1n') and contains(@class, 'xxbr6pl') and contains(@class, 'x1n2onr6') and contains(@class, 'x1rg5ohu') and contains(@class, 'xk50ysn') and contains(@class, 'x1f6kntn') and contains(@class, 'xyesn5m') and contains(@class, 'x1z11no5') and contains(@class, 'xjy5m1g') and contains(@class, 'x1mnwbp6') and contains(@class, 'x4pb5v6') and contains(@class, 'x178xt8z') and contains(@class, 'xm81vs4') and contains(@class, 'xso031l') and contains(@class, 'xy80clv') and contains(@class, 'x13fuv20') and contains(@class, 'xu3j5b3') and contains(@class, 'x1q0q8m5') and contains(@class, 'x26u7qi') and contains(@class, 'x1v8p93f') and contains(@class, 'xogb00i') and contains(@class, 'x16stqrj') and contains(@class, 'x1ftr3km') and contains(@class, 'x1hl8ikr') and contains(@class, 'xfagghw') and contains(@class, 'x9dyr19') and contains(@class, 'x9lcvmn') and contains(@class, 'xbtce8p') and contains(@class, 'x14v0smp') and contains(@class, 'xo8ufso') and contains(@class, 'xcjl5na') and contains(@class, 'x1k3x3db') and contains(@class, 'xuxw1ft') and contains(@class, 'xv52azi')]"))
            )
            ok_button.click()
            print("Clicked 'OK' on the popup.")
    
            # Wait for and click the "Chats" div
            print("Waiting for the 'Chats' div to be clickable.")
            chats_div = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Chats' and @role='button']"))
            )
            chats_div.click()
            print("Clicked on the 'Chats' div to open chats.")
            
            # Capture screenshots and save to PDF
            chat_screenshots = take_chat_screenshots(driver)
            if chat_screenshots:
                generate_pdf(chat_screenshots, filename="whatsapp_chats.pdf")
                print("Saved chat screenshots to whatsapp_chats.pdf")
            else:
                print("No chat screenshots were taken.")
            
        except TimeoutException as e:
            print(f"Error: Timeout while waiting for an element. Details: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
        
def take_chat_screenshots(driver):
    screenshots = []
    try:
        # Wait for the chat list to load
        chat_list = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Chat list' and @role='grid']"))
        )
        print("Chat list loaded successfully.")

        # Get all chat elements
        chat_elements = chat_list.find_elements(By.XPATH, ".//div[@role='listitem']")
        print(f"Found {len(chat_elements)} chats.")

        for i, chat in enumerate(chat_elements):
            try:
                chat.click()  # Open the chat
                random_delay(2, 2)  # Fixed delay of 3 seconds before taking the screenshot

                # Capture a screenshot after opening the chat
                screenshot_filename = f'chat_screenshot_{i + 1}.png'
                driver.save_screenshot(screenshot_filename)
                screenshots.append(screenshot_filename)
                print(f"Screenshot taken: {screenshot_filename}")

                # Scroll through chat if needed
                chat_container = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "(//div[contains(@class, 'x10l6tqk') and contains(@class, 'x13vifvy') and contains(@class, 'x17qophe') and contains(@class, 'xyw6214') and contains(@class, 'x9f619') and contains(@class, 'x78zum5') and contains(@class, 'xdt5ytf') and contains(@class, 'xh8yej3') and contains(@class, 'x5yr21d') and contains(@class, 'x6ikm8r') and contains(@class, 'x1rife3k') and contains(@class, 'xjbqb8w') and contains(@class, 'x1ewm37j')])")
                    )
                )

                # Check if the chat container is scrollable
                scroll_height = driver.execute_script("return arguments[0].scrollHeight", chat_container)
                client_height = driver.execute_script("return arguments[0].clientHeight", chat_container)

                while True:
                    if scroll_height <= client_height:
                        print("No more content to scroll.")
                        break

                    # Detect if the "synced older message" button appears
                    # try:
                    #     synced_older_msg_button = WebDriverWait(driver, 5).until(
                    #         EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'x14m1o6m') and contains(@class, 'x150wa6m') and contains(@class, 'x1b9z3ur') and contains(@class, 'x9f619')]"))
                    #     )
                    #     print("Synced older message button found. Waiting for it to disappear.")
                        
                    #     # Wait for the button to disappear
                    #     WebDriverWait(driver, 20).until(
                    #         EC.invisibility_of_element(synced_older_msg_button)
                    #     )
                    #     print("Synced older message button disappeared. Continuing scroll.")
                    # except TimeoutException:
                    #     print("No synced older message button appeared. Continuing scroll.")

                    # Take a screenshot while scrolling
                    screenshot_filename = f'chat_screenshot_{i + 1}_scroll.png'
                    driver.save_screenshot(screenshot_filename)
                    screenshots.append(screenshot_filename)
                    print(f"Screenshot taken while scrolling: {screenshot_filename}")

                    # Scroll up (adjusting the scroll height)
                    driver.execute_script("arguments[0].scrollTop -= arguments[1];", chat_container, client_height)
                    random_delay(2, 4)  # Wait for the messages to load

                    # Update scroll height
                    current_scroll_position = driver.execute_script("return arguments[0].scrollTop;", chat_container)
                    if current_scroll_position == 0:
                        print("Reached the top of the chat.")
                        break

                # Go back to the chat list
                driver.back()
                random_delay(2, 4)  # Wait for the chat list to reload

                # Ensure the next chat is clickable by waiting for the chat list to refresh
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Chat list' and @role='grid']"))
                )
                print("Back to chat list, moving to the next chat.")

            except Exception as e:
                print(f"Error with chat {i + 1}: {e}")
                continue  # Proceed with the next chat even if there's an error with the current one

    except Exception as e:
        print(f"An error occurred: {e}")

    return screenshots

def generate_pdf(screenshots, filename="whatsapp_chats.pdf"):
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
        # Initialize the WebDriver and log in
        login_to_whatsapp(driver)

        # Take screenshots of chats
        chat_screenshots = take_chat_screenshots(driver)

        # Generate PDF from chat screenshots
        if chat_screenshots:
            generate_pdf(chat_screenshots, filename="whatsapp_chats.pdf")
            print("Saved chat screenshots to whatsapp_chats.pdf")
        else:
            print("No chat screenshots were taken.")

    finally:
        driver.quit()  # Ensure the driver is closed after execution
