import time
import random
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Create ChromeOptions object and set incognito mode and user agent
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")

# Create a new instance of the Chrome driver with the options
driver = webdriver.Chrome(options=options)

# Navigate to the page
driver.get("https://www.funda.nl/en/koop/utrecht/")

# Add a random delay before accepting cookies
time.sleep(random.uniform(1.5, 3.5))

# Scroll the page
scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
driver.execute_script("window.scrollTo(0, {})".format(random.randint(0, scroll_height)))

# Wait for the accept cookies button to be clickable
wait = WebDriverWait(driver, 10)
accept_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[id="onetrust-button-group-parent"] > div > div > button[id="onetrust-accept-btn-handler"]')))

# Move the mouse pointer to the accept cookies button
actions = ActionChains(driver)
actions.move_to_element(accept_button).perform()
time.sleep(random.uniform(0.5, 1.5))

# Click the accept cookies button
accept_button.click()
print("Button clicked, now waiting for 60 seconds")
time.sleep(60)

# Scrape information from listings on the current page and store in CSV
def scrape_listings():
    listings = driver.find_elements(By.CSS_SELECTOR, 'div.p-4 div[data-test-id="search-result-item"] > div > div > div.flex.justify-between')
    with open("listings.csv", "a", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        for listing in listings:
            # title_element = listing.find_element(By.CSS_SELECTOR, 'a.search-result-header__title')
            title = listing.text
            # Convert the listing into a single line
            lines = title.split('\n')
            listing_line = ",".join(lines)
            csv_writer.writerow([listing_line])

# Initial scraping of the first page
scrape_listings()

# Check if there is a "Volgende" (Next) button and click it if available
while True:
    next_button = driver.find_element(By.XPATH, '//li[@data-v-b8a43de0=""]//span[text()="Volgende"]/..')
    if next_button.is_enabled():
        next_button.click()
        print("Clicked on the 'Volgende' (Next) button, now waiting for 60 seconds before scraping the next page")
        time.sleep(random.uniform(10,25))
        scrape_listings()
    else:
        print("No more pages to scrape. Exiting...")
        break

# Close the browser
# driver.quit()
