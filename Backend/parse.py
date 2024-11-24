from flask import Flask, request, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.common.by import By
import PyPDF2
import io
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Platform configurations for login
PLATFORM_CONFIG = {
    "facebook": {
        "url": "https://www.facebook.com/",
        "username_field": {"by": By.ID, "value": "email"},
        "password_field": {"by": By.ID, "value": "pass"},
        "login_button": {"by": By.NAME, "value": "login"},
        "success_indicator": {"by": By.XPATH, "value": "//div[contains(@class, 'x1n2onr6')]"},
    },
    "instagram": {
        "url": "https://www.instagram.com/accounts/login/",
        "username_field": {"by": By.NAME, "value": "username"},
        "password_field": {"by": By.NAME, "value": "password"},
        "login_button": {"by": By.XPATH, "value": "//button[@type='submit']"},
        "success_indicator": {"by": By.XPATH, "value": "//div[contains(@class, 'x1n2onr6')]"},
    },
    "twitter": {
        "url": "https://x.com/i/flow/login",
        "username_field": {"by": By.NAME, "value": "text"},
        "password_field": {"by": By.NAME, "value": "password"},
        "login_button": {"by": By.XPATH, "value": "//button[@role='button']"},
        "success_indicator": {"by": By.XPATH, "value": "//a[@aria-label='Home' and @role='link']"},
    },
    "gmail": {
        "url": "https://accounts.google.com/signin",
        "username_field": {"by": By.ID, "value": "identifierId"},
        "password_field": {"by": By.NAME, "value": "password"},
        "login_button": {"by": By.ID, "value": "identifierNext"},
        "success_indicator": {"by": By.XPATH, "value": "//img[@class='gb_uc']"},
    },
}

# Route for login functionality
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    platform = data.get('platform')
    username = data.get('username')
    password = data.get('password')

    if not platform or platform not in PLATFORM_CONFIG:
        return jsonify({'success': False, 'message': f'Platform {platform} not supported'}), 400
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400

    try:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)

        config = PLATFORM_CONFIG[platform]
        driver.get(config["url"])

        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((config["username_field"]["by"], config["username_field"]["value"])))
        username_field.send_keys(username)

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((config["password_field"]["by"], config["password_field"]["value"])))
        password_field.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((config["login_button"]["by"], config["login_button"]["value"])))
        login_button.click()

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((config["success_indicator"]["by"], config["success_indicator"]["value"])))
            success = True
        except:
            success = False

        driver.quit()

        if success:
            return jsonify({'success': True, 'message': 'Login successful'}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# Route for parsing functionality
@app.route('/parse', methods=['POST'])
def parse_data():
    try:
        # Parse request data
        data = request.get_json()
        platform = data.get('platform')
        username = data.get('username')
        password = data.get('password')
        option = data.get('option')

        if not platform or not username or not password or not option:
            return jsonify({'message': 'Missing required fields'}), 400

        platform_scripts = {
            "facebook": {
                "Parse Followers": 'c:\\Users\\sarth\\Desktop\\project_2\\Backend\\sih_facebook.py',
                "Parse Posts": 'c:\\Users\\sarth\\Desktop\\project_2\\Backend\\sih_facebook_posts.py',
                "Parse Chats": 'c:\\Users\\sarth\\Desktop\\project_2\\Backend\\sih_facebook_chats.py',
            },
            "instagram": {
                "Parse Followers": 'c:\\path\\to\\instagram_followers.py',
                "Parse Posts": 'c:\\path\\to\\instagram_posts.py',
                "Parse Chats": 'c:\\path\\to\\instagram_chats.py',
            },
            "twitter": {
                "Parse Followers": 'c:\\path\\to\\twitter_followers.py',
                "Parse Posts": 'c:\\path\\to\\twitter_posts.py',
                "Parse Chats": 'c:\\path\\to\\twitter_chats.py',
            },
            "gmail": {
                "Parse Followers": 'c:\\path\\to\\gmail_followers.py',
                "Parse Posts": 'c:\\path\\to\\gmail_posts.py',
                "Parse Chats": 'c:\\path\\to\\gmail_chats.py',
            }
        }

        # Check for "Parse All" option
        if option == 'Parse All':
            options_to_parse = ["Parse Followers", "Parse Posts", "Parse Chats"]
            pdf_writer = PyPDF2.PdfWriter()  # Create a PDF writer to merge all PDFs

            for plat, scripts in platform_scripts.items():
                if plat == platform:  # Only run for selected platform
                    for option_to_parse in options_to_parse:
                        script_path = scripts.get(option_to_parse)
                        if script_path:
                            print(f"Running script for {option_to_parse} for {platform}...")
                            # Run the script for each option
                            command = ['python', script_path, username, password]
                            process = subprocess.run(command, capture_output=True)

                            if process.returncode != 0:
                                error_message = process.stderr.decode()
                                return jsonify({'message': error_message}), 400

                            # Assuming each script returns a PDF as output
                            pdf_data = io.BytesIO(process.stdout)  # Convert to byte stream
                            pdf_reader = PyPDF2.PdfReader(pdf_data)  # Read the PDF
                            
                            # Merge the PDF
                            for page in range(len(pdf_reader.pages)):
                                pdf_writer.add_page(pdf_reader.pages[page])

            # Prepare the combined PDF in memory
            combined_pdf = io.BytesIO()
            pdf_writer.write(combined_pdf)
            combined_pdf.seek(0)  # Go to the beginning of the combined PDF

            # Send the combined PDF file as a response
            return send_file(
                combined_pdf,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'{platform}_Parse_All.pdf'
            )

        else:
            # Parse the selected individual option (if not "Parse All")
            if platform in platform_scripts and option in platform_scripts[platform]:
                script_path = platform_scripts[platform][option]
                command = ['python', script_path, username, password]
                process = subprocess.run(command, capture_output=True)

                if process.returncode != 0:
                    error_message = process.stderr.decode()
                    return jsonify({'message': error_message}), 400

                # Send the individual PDF file as a response
                pdf_data = io.BytesIO(process.stdout)  # Assuming the output is a PDF
                return send_file(
                    pdf_data,
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=f'{platform}_{option.replace(" ", "_")}.pdf'
                )
            else:
                return jsonify({'success': False, 'message': 'Invalid option selected.'}), 400

    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
