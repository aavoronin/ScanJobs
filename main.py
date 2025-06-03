import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# === CONFIG ===
CHROMEDRIVER_PATH = "C:/chromedriver/chromedriver.exe"  # Change this path

# === CHROME OPTIONS ===
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# === START BROWSER ===
service = Service(CHROMEDRIVER_PATH)
#driver = webdriver.Chrome(service=service, options=chrome_options)
# Automatically downloads the correct ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# === OPEN LINKEDIN ===
driver.get("https://www.linkedin.com")
time.sleep(5)  # Let the page load

# === GET INNER HTML ===
html_content = driver.execute_script("return document.documentElement.innerHTML;")

# === PRINT OR SAVE ===
print(html_content[:1000])  # Print the first 1000 characters
# Optionally save to file
with open("linkedin_page.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# === CLEANUP ===
# driver.quit()
