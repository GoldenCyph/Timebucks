from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to perform the task actions
def perform_task(num_posts):
    # Initialize the WebDriver (assuming Chrome)
    driver = webdriver.Chrome()
    driver.get("https://bit.ly/3I74m3Z")

    try:
        # Check if the "Follow Link" button is present
        follow_button_present = EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Follow Link"))

        try:
            if follow_button_present(driver):
                # Wait for the "Follow Link" button to be located and click it
                follow_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Follow Link"))
                )
                follow_button.click()

                # Wait for the page to load
                time.sleep(5)
        except:
            print("No 'Follow Link' button found. Proceeding directly to clicking on posts.")

        # Click on the specified number of posts plus 2 additional posts on the site using modified XPath expressions
        for i in range(1, num_posts + 3):
            post_xpath = f'(//a[@rel="bookmark"])[{i}]'
            try:
                post = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, post_xpath))
                )
                print(f"Clicking on post {i}")
                post.click()
                time.sleep(5)  # Wait for the page to load completely

            except:
                print(f"Unable to click on post {i} due to ad blocking. Skipping to the next post.")
                continue

            # If it's not the last post, go back to the previous page
            if i != num_posts + 2:
                driver.execute_script("window.history.go(-1)")

        print("Task completed successfully.")

    except Exception as e:
        print(f"Unable to perform the task: {e}")

    finally:
        # Close the WebDriver
        driver.quit()

# Call the function to perform the task with the desired number of posts
perform_task(5)  # Change the number as needed