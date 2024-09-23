from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import json
import time
import re

# Set up Flask
app = Flask(__name__)

# Geckodriver path
geckodriver_path = 'geckodriver'  # Update this path if necessary

def scroll_slowly(driver, scroll_pause_time=2, scroll_increment=300):
    """Scrolls the page slowly up and down to load all images."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(scroll_pause_time)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(f"window.scrollBy(0, -{scroll_increment});")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def clean_url(url):
    """Remove query parameters and add /photos to the URL."""
    if url:
        base_url = re.sub(r'\?zrp_bid=\d+&zrp_pid=\d+', '', url)
        return base_url + '/photos'
    return url

def clean_image_url(url):
    """Remove everything after the question mark in the URL."""
    if url:
        return url.split('?')[0]
    return url

def get_image_sources(driver, url):
    driver.get(url)
    scroll_slowly(driver)

    wait = WebDriverWait(driver, 60)
    try:
        img_elements = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'img.sc-s1isp7-5.eisbVA')))
        return [clean_image_url(img_element.get_attribute('src')) for img_element in img_elements]
    except Exception as e:
        print(f"Error finding images: {e}")
        return []

def get_feature_image(driver, url):
    driver.get(url)
    
    wait = WebDriverWait(driver, 40)
    
    try:
        feature_img_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.sc-s1isp7-5.eQUAyn')))
        return clean_image_url(feature_img_element.get_attribute('src'))
    except Exception as e:
        print(f"Error finding feature image: {e}")
        return ""

@app.route('/process', methods=['POST'])
def process_json():
    # Start a headless Firefox session
    firefox_options = FirefoxOptions()
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--disable-dev-shm-usage')
    firefox_options.add_argument('--disable-gpu')

    service = Service(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        # Receive JSON from the request
        data = request.get_json()

        # Process the URLs and images
        for key in data:
            for item in data[key]:
                if 'url' in item:
                    url = clean_url(item['url'])
                    print(f"Processing URL: {url}")

                    image_sources = get_image_sources(driver, url)
                    feature_image = get_feature_image(driver, url)
                    
                    if 'images' not in item:
                        item['images'] = []
                    item['images'].extend(image_sources)
                    item['feature_image'] = feature_image

        # Send back the updated data
        return jsonify(data)

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
