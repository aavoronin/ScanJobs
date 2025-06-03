import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Kill any running Chrome processes
os.system("taskkill /im chrome.exe /f")
os.system("taskkill /im chromedriver.exe /f")
time.sleep(5)  # Wait for Chrome to close

# Path to your existing Chrome user data (with Browsec installed)
USER_DATA_DIR = r"C:\Users\alexe\AppData\Local\Google\Chrome\User Data"
PROFILE_DIR = "Default"

# Ensure profile path exists
profile_path = os.path.join(USER_DATA_DIR, PROFILE_DIR)
if not os.path.exists(profile_path):
    os.makedirs(profile_path)

# Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
chrome_options.add_argument(f"--profile-directory={PROFILE_DIR}")
chrome_options.add_argument("--remote-debugging-port=9222")  # 🔧 IMPORTANT FIX
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-session-crashed-bubble")
chrome_options.add_argument("--disable-features=InfiniteSessionRestore")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# Start Chrome using ChromeDriverManager to avoid version mismatch
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Wait for Browsec to auto-connect
driver.get("https://www.google.com")
print("Opened URL:", driver.current_url)
time.sleep(8)

# Go to LinkedIn
driver.get("https://www.linkedin.com")
print("Opened URL:", driver.current_url)
time.sleep(5)

# Save page content
html_content = driver.execute_script("return document.documentElement.innerHTML;")
print(html_content[:1000])
with open("linkedin_page.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Optional: driver.quit()
