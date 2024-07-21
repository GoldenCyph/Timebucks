from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import random
import cv2
import pytesseract

def handle_captcha_manually():
    print("A CAPTCHA has appeared. Please solve it manually.")
    print("Once solved, press Enter to continue...")
    input()

def extract_captcha_text_from_screenshot(screenshot_path):
    # Read the screenshot
    img = cv2.imread(screenshot_path)

    # Preprocess the image (e.g., resize, convert to grayscale)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply any other preprocessing steps as needed

    # Use pytesseract to perform OCR on the preprocessed image
    captcha_text = pytesseract.image_to_string(gray)

    return captcha_text

def automate_timebucks_login(email, password):
    driver = webdriver.Chrome()
    try:
        driver.get('https://timebucks.com/')

        # Wait for the email field to be visible
        email_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'username_box')))
        email_field.send_keys(email)

        # Find the password field and fill it in with your password
        password_field = driver.find_element(By.ID, 'password_box')
        password_field.send_keys(password)

        # Find the login button and click it
        login_button = driver.find_element(By.XPATH, '//input[@value="Log In"]')
        login_button.click()

        # Wait for a few seconds to ensure the page loads properly
        time.sleep(5)

        # Handle browser notification prompt if it appears
        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert.accept()
        except:
            pass

        # Click on the menu icon
        print("Clicking on the menu icon...")
        menu_icon = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.jsc-sidebar-trigger')))
        menu_icon.click()

        # Click on the "Earn" section
        print("Clicking on the 'Earn' section link...")
        earn_section_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Earn"]')))
        earn_section_link.click()

        # Wait for a few seconds to ensure the page loads properly
        time.sleep(2)

        # Automate tasks section
        automate_timebucks_tasks(driver)

    except NoSuchElementException as e:
        print(f"Error: {e}")
        print("Menu icon or Earn section link not found. Unable to proceed.")

    finally:
        # Close the browser window after completing the tasks
        driver.quit()

def extract_and_store_task_texts(driver, ad_instructions_xpath, proof_instructions_xpath, proof_completion_xpath):
    # Extract text content from the provided XPaths
    ad_instructions_element = driver.find_element(By.XPATH, ad_instructions_xpath)
    proof_instructions_element = driver.find_element(By.XPATH, proof_instructions_xpath)
    proof_completion_element = driver.find_element(By.XPATH, proof_completion_xpath)
    
    # Get the text content of each element
    ad_instructions_text = ad_instructions_element.text.strip()
    proof_instructions_text = proof_instructions_element.text.strip()
    proof_completion_text = proof_completion_element.text.strip()
    
    # Store the texts for further use
    task_texts = {
        "ad_instructions": ad_instructions_text,
        "proof_instructions": proof_instructions_text,
        "proof_completion": proof_completion_text
    }
    
    return task_texts

def automate_timebucks_tasks(driver):
    # Click on the tasks section
    tasks_tile = driver.find_element(By.ID, 'tasks')
    tasks_tile.click()

    # Wait for the tasks to be fully loaded
    print("Waiting for tasks to be fully loaded...")
    time.sleep(20)

    # Locate the main frame containing all tasks
    main_frame = driver.find_element(By.ID, 'tblBuyReferrals')

    # Extract text from the main frame
    main_frame_text = main_frame.text

    # List of desired task titles
    desired_titles = [
        "Engage on my Website",
        "Visit website Engage with Website",
        "Website Visit Engage",
        "Website visit and Engage",
        "Visit & Engage with Blog",
        "Visit website Engage",
        "Website Visit + Engage",
        "Website visit and Engagement",
        "Website visit and engagement",
        "Simple Visit, Click and Earn",
        "Visit website, Engage with Website and get paid",
        "View web and engage",
        "Earn extra Cash",
        "Browse my website",
        "Visit my website and Engage with Websites",
        "Visit my website and earn rewards daily",
        "Website Visit and engagements",
        "Website visit and engage",
        "Visit My website, Engage and Earn Instantly",
        "Visit plus Browse my website",
        "Visit website",
        "Browse and Engage my website",
        "Visit Site Engage",
        "Visit website Engage with Website",
        "Vist my site",
        "Visit to a website and Engage",
        "Visit + Engage",
        "Visit and engage",
        "Website visit & engage",
        "Engage With A website And Get Paid",
    ]

    # Print the desired task titles
    print("Desired task titles:")
    print(desired_titles)

    # Shuffle the list of desired task titles
    random.shuffle(desired_titles)

    # Search for the desired task titles within the main frame text
    found_titles = []
    for title in desired_titles:
        if title in main_frame_text:
            found_titles.append(title)

    # Print the found task titles
    print("Found task titles:")
    if found_titles:
        for found_title in found_titles:
            print(found_title)
    else:
        print("No desired task titles found.")

    # Iterate through each mini frame within the main frame
    for i in range(1, 4):  # Assuming there are 3 mini frames
        mini_frame_xpath = f'//*[@id="tblBuyReferrals"]/tbody/tr[{i}]/td[2]'
        mini_frame = main_frame.find_element(By.XPATH, mini_frame_xpath)

        # Locate view buttons within the mini frame
        view_buttons_xpath = f'{mini_frame_xpath}/center/a/span/input'
        view_buttons = mini_frame.find_elements(By.XPATH, view_buttons_xpath)

        # If there are view buttons, click on one randomly
        if view_buttons:
            random_view_button = random.choice(view_buttons)
            random_view_button.click()
            print(f"Clicked on a random view button for one of the desired tasks in mini frame {i}")

            # Pause the script to simulate waiting on the new page
            time.sleep(10)  # Wait for 10 seconds

            # Check if the "Start Campaign" button appears as a captcha
            try:
                captcha_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]')))
                if captcha_button.is_displayed():
                    print("Captcha detected.")
                    handle_captcha_manually()
                    # After handling the CAPTCHA, you may need to refresh the page or take other actions to continue
                    continue
            except TimeoutException:
                # No captcha detected, continue with other actions
                pass

            # After clicking on the "Start Campaign" button or manually solving the captcha
            ad_instructions_xpath = '//*[@id="tasks_content_375"]/div[5]/div[3]/div[4]/p[2]'
            proof_instructions_xpath = '//*[@id="tasks_content_375"]/div[5]/div[3]/div[5]/p'
            proof_completion_xpath = '//*[@id="tasks_content_375"]/div[5]/div[3]/div[6]/p[3]'

            task_texts = extract_and_store_task_texts(driver, ad_instructions_xpath, proof_instructions_xpath, proof_completion_xpath)
            print("Task texts:", task_texts)

            # Exit loop after clicking one view button
            break

        # Pause to allow more time for solving captcha and clicking verify button
        time.sleep(10)  # Adjust the sleep time as needed

# Use your login details to automate the login process
email = "olaawoniyi8@gmail.com"
password = "Trickstarz2#"

automate_timebucks_login(email, password)
