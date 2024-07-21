from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import random

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

def filter_task(task_texts, exclude_keywords):
    # Check if any exclude keyword is present in task titles or instructions
    for keyword in exclude_keywords:
        if (keyword in task_texts["ad_instructions"].lower()) or (keyword in task_texts["proof_instructions"].lower()):
            print(f"Task contains '{keyword}'. Skipping...")
            return True  # Exclude task
    return False  # Include task

def automate_timebucks_tasks(driver, exclude_keywords=["quiz", "game", "play", "win", "coins", "games"]):
    # Click on the tasks section
    tasks_tile = driver.find_element(By.ID, 'tasks')
    tasks_tile.click()

    while True:
        # Wait for the tasks to be fully loaded
        print("Waiting for tasks to be fully loaded...")
        time.sleep(20)

        # Check for campaign expired popup
        try:
            popup = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "swal2-popup")]')))
            if popup.is_displayed():
                print("Campaign expired popup detected. Closing it...")
                close_button = driver.find_element(By.XPATH, '//button[@class="swal2-cancel btn btn-danger"]')
                close_button.click()
                print("Popup closed.")
                # Click on the "Back To Tasks" button
                back_to_tasks_button_xpath = '/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div[5]/div[2]/p[2]/span/a'
                back_to_tasks_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, back_to_tasks_button_xpath)))
                back_to_tasks_button.click()
                print("Clicked on 'Back To Tasks' button.")
                # Break the loop and check for tasks again
                break
        except TimeoutException:
            pass

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
                # You can adjust the wait time as needed
                time.sleep(10)  # Wait for 10 seconds

                # Check if the "Start Campaign" button appears as a captcha
                try:
                    captcha_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]')))
                    if captcha_button.is_displayed():
                        print("Captcha detected. Please solve it manually.")
                        input("Press Enter to continue after solving the captcha...")
                        # After solving the captcha, we need to check again for the "Start Campaign" button
                        continue
                except TimeoutException:
                    # No captcha detected, continue with other actions
                    pass

                # Check if the "Start Campaign" button appears
                start_campaign_button_xpath = '/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div[5]/div[2]/div[4]/span'
                try:
                    start_campaign_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, start_campaign_button_xpath)))
                    if start_campaign_button.is_displayed():
                        print("Start Campaign button detected. Clicking it...")
                        start_campaign_button.click()
                        # Add a delay after clicking the button to ensure the page fully loads
                        time.sleep(5)
                except TimeoutException:
                    # "Start Campaign" button not found, continue with other actions
                    pass

                # After clicking on the "Start Campaign" button or manually solving the captcha
                ad_instructions_xpath = '//*[@id="tasks_content_375"]/div[5]/div[3]/div[4]/p[2]'
                proof_instructions_xpath = '//*[@id="tasks_content_375"]/div[5]/div[3]/div[5]/p'
                proof_completion_xpath = '//*[@id="tasks_content_375"]/div[5]/div[3]/div[6]/p[3]'

                task_texts = extract_and_store_task_texts(driver, ad_instructions_xpath, proof_instructions_xpath, proof_completion_xpath)
                print("Task texts:", task_texts)

                # Filter out tasks containing exclude keywords
                if filter_task(task_texts, exclude_keywords):
                    # Click on the "Back To Tasks" button
                    back_to_tasks_button_xpath = '/html/body/div[9]/div[3]/div/div[2]/div[2]/div[1]/div/div[4]/div/div/div[1]/div[5]/div[2]/p[2]/span/a'
                    back_to_tasks_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, back_to_tasks_button_xpath)))
                    back_to_tasks_button.click()
                    print("Clicked on 'Back To Tasks' button.")
                    # Break the loop and check for tasks again
                    break

                # Process the task further if not excluded
                print("Running task instructions...")
                print("ad_instructions:", task_texts["ad_instructions"])
                print("proof_instructions:", task_texts["proof_instructions"])
                print("proof_completion:", task_texts["proof_completion"])

                # Extract the URL from the ad_instructions
                url_start_index = task_texts["ad_instructions"].find("https://")
                url_end_index = task_texts["ad_instructions"].find("\n", url_start_index)
                url = task_texts["ad_instructions"][url_start_index:url_end_index]

                # Open the URL in a new tab
                driver.execute_script(f"window.open('{url}','_blank')")

                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[1])

                # Wait for the page to load
                time.sleep(5)  # Adjust as needed

                # Now you can proceed with the rest of the task instructions

                # Exit loop after clicking one view button
                break

            # Pause to allow more time for solving captcha and clicking verify button
            time.sleep(10)  # Adjust the sleep time as needed
        else:
            # No view buttons found in all mini frames, break the loop
            break

# Use your login details to automate the login process
email = "bukunmiadetunji1@gmail.com"
password = "Abouttogetr11ch"

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
    # Allow the URL to finish loading before quitting
    time.sleep(10)  # Adjust the wait time as needed
    # Close the browser window after completing the tasks
    driver.quit()
