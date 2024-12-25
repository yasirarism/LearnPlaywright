from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from logging import getLogger, FileHandler, StreamHandler, INFO, basicConfig
from urllib.parse import urlparse
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)

basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[FileHandler("log.txt"), StreamHandler()],
    level=INFO,
)

LOGGER = getLogger(__name__)

def wait_for_page_load(driver):
    """Wait until the page is fully loaded by checking document.readyState"""
    wait = WebDriverWait(driver, 30)
    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

@app.get("/")
def halo():
    return jsonify({"message": "Haloo"})

@app.route('/dood', methods=['GET'])
def get_video_url():
    # Get the URL parameter from the request
    dood_url = request.args.get('url')

    if not dood_url:
        return jsonify({"error": "URL parameter is required"}), 400

    if '/d/' in dood_url:
        dood_url = dood_url.replace('/d/', '/e/')

    domain = urlparse(dood_url).netloc

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--proxy-server=http://103.148.130.107:8080")
    options.add_argument(f"user-agent=Mozilla/5.0 (Linux; Android 15; Pixel 9 Pro Fold Build/AP3A.241005.015; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/129.0.6668.100 Mobile Safari/537.36")

    # Use Chromium instead of Chrome
    options.binary_location = "/usr/bin/google-chrome"

    # Specify the path to ChromiumDriver
    driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver-linux64/chromedriver"), options=options)

    try:
        driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
            'headers': {
                'Referer': f'https://{domain}/'
            }
        })

        driver.get(dood_url)
        # wait_for_page_load(driver)
        # LOGGER.info(driver.page_source)
        time.sleep(5)
   
        video_url = None
        try:
            video_element = driver.find_element(By.XPATH, "//video")
            video_url = video_element.get_attribute("src")
        except Exception as e:
            LOGGER.error(f"1, {e}")
            return jsonify({"error": "Video URL not found", "message": str(e)}), 404

        video_title = driver.title

        if video_url:
            return jsonify({
                "success": True,
                "video_url": video_url,
                "referer": domain,
                "title": video_title
            })
        else:
            LOGGER.error("2")
            return jsonify({"error": "Video URL not found"}), 404

    except Exception as e:
        LOGGER.error(f"3, {e}")
        return jsonify({"error": "Error fetching the page", "message": str(e)}), 500

    finally:
        driver.quit()  # Close the driver

# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=8081)
    
dood_app = WsgiToAsgi(app)
