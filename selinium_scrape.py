from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Your data
data = {'title': 'some title', 'body': 'somebodyy'}

# Path to your webdriver (replace with your actual webdriver path)
driver_path = "path/to/your/chromedriver"

# Start a browser session
driver = webdriver.Chrome(driver_path)

# Open Reddit's post creation page
driver.get("https://www.reddit.com/submit?type=TEXT")

# Give the page some time to load
time.sleep(5)

# Autofill the title
title_field = driver.find_element(By.TAG_NAME, "input")  # Finds the title input field
title_field.send_keys(data['title'])

# Autofill the body
body_field = driver.find_element(By.TAG_NAME, "textarea")  # Finds the body textarea
body_field.send_keys(data['body'])

# Done! The fields should now be autofilled
print("Autofill complete. Check your browser.")

# Keep the browser open for you to review
time.sleep(30)

# Close the browser
driver.quit()
