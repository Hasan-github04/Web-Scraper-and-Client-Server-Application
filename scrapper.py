from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()
driver.get("https://www.rit.edu/dubai/directory")

for _ in range(5):
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "see-more"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
        load_more_button.click()
        print("Clicked 'Load More' button.")
        time.sleep(2)
    except Exception as e:
        print(f"Error loading more employees: {e}")
        break

page_source = driver.page_source
driver.quit()

soup = BeautifulSoup(page_source, 'html.parser')

directory_entries = soup.find_all('div', class_='person--info')  

data = []
for entry in directory_entries:

    name_tag = entry.find('div', class_='pb-2').find('a')
    name = name_tag.text.strip() if name_tag else None

    title_tag = entry.find('div', class_='pb-2 directory-text-small')
    title = title_tag.text.strip() if title_tag else None
    
    data.append({'Name': name, 'Title': title})


df = pd.DataFrame(data)

email = [e.getText().strip() for e in soup.find_all(class_="pb-2 directory-text-small") if e.find("a")]
df['Email'] = email

df.to_csv("directory.csv", index=False)

print("Data successfully saved to 'directory.csv'.")
