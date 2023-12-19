from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import redis

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://gamerant.com/gaming/")

# Assuming article titles are within <h2> tags
article_titles = driver.find_elements(By.CLASS_NAME, "display-card-title ")

# Writing data to a text file
with open("articles.txt", "w", encoding="utf-8") as file:
    title_index = 0
    max_attempts = 5  # Set a maximum number of attempts

    while title_index < len(article_titles) and title_index < max_attempts:
        try:
            # Re-find the article titles in each iteration
            article_titles = driver.find_elements(By.CLASS_NAME, "display-card-title ")

            # Scroll to bring the element into view
            driver.execute_script("arguments[0].scrollIntoView();", article_titles[title_index])
            time.sleep(1)  # Give the page some time to adjust

            # Click on each article title
            article_titles[title_index].click()

            # Wait for the article details to be visible
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "content-block-regular")))

            # Get article title
            article_title = driver.find_element(By.CLASS_NAME, "heading_title").text

            # Get article image source
            img = driver.find_element(By.TAG_NAME, "img")
            article_img = img.get_attribute("src") if img else "No image"

            # Get all <p> tags within the article details
            article_details_container = driver.find_element(By.CLASS_NAME, "content-block-regular")
            article_details_elements = article_details_container.find_elements(By.TAG_NAME, "p")
            article_details_texts = [element.text for element in article_details_elements]

            # Write title, image, and details to the file
            file.write(f"Title: {article_title}\n")
            file.write(f"Image Source: {article_img}\n")
            file.write("Details:\n")
            for detail_text in article_details_texts:
                file.write(f"- {detail_text}\n")
            file.write("=" * 50 + "\n")  # Adding a separator between articles

            # Serialize the data into JSON before storing in Redis
            article_data = {
                "title": article_title,
                "image_source": article_img,
                "details": article_details_texts,
            }
            json_data = json.dumps(article_data)

            # Store in Redis with an expiration of 3 days (259200 seconds)
            redis_key = f"article:{title_index}"
            redis_client.setex(redis_key, 259200, json_data)

            title_index += 1  # Move to the next article

        except Exception as e:
            print(f"Error processing article: {e}")

        finally:
            # Go back to the main page
            driver.back()
            time.sleep(2)  # Give the page some time to load

driver.quit()
