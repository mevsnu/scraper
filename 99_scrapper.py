import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the Chrome driver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (without opening the browser)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Scrape 99acres for the society's data
def scrape_society_data(society_name):
    driver = setup_driver()
    try:
        # Navigate to 99acres.com
        driver.get("https://www.99acres.com")
        
        # Wait for the search box to be present
        wait = WebDriverWait(driver, 10)
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search by City, Locality, Project or Society Name']")))
        
        # Input the society's name into the search bar
        search_box.send_keys(society_name)
        search_box.submit()
        
        time.sleep(3)  # Allow time for the results to load

        # Scrape the results (assuming the first search result is relevant)
        society_data = []
        posts = driver.find_elements(By.CLASS_NAME, "srpTuple__tupleTable")

        for post in posts:
            try:
                title = post.find_element(By.ID, "srp_tuple_property_title").text.strip()
                price = post.find_element(By.ID, "srp_tuple_price").text.strip()
                area = post.find_element(By.ID, "srp_tuple_primary_area").text.strip()
                bed = post.find_element(By.ID, "srp_tuple_bedroom").text.strip()
                moves = post.find_element(By.CLASS_NAME, "badges__secondaryLargeSubtle").text.strip()
                
                society_data.append({
                    "Title": title,
                    "Price": price,
                    "Super Area": area,
                    "BHK": bed,
                    "Move-in Status": moves
                })
            except:
                # In case any element is not found, continue with next post
                continue
        
        # Convert to DataFrame
        if society_data:
            df = pd.DataFrame(society_data)
            # Save to Excel
            df.to_excel(f"{society_name}_99acres_data.xlsx", index=False)
            print(f"Data saved to {society_name}_99acres_data.xlsx")
        else:
            print(f"No data found for the society '{society_name}'")
    
    finally:
        driver.quit()

# Main function
if __name__ == "__main__":
    society_name = input("Enter the society's name to search on 99acres: ")
    scrape_society_data(society_name)
