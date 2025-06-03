import os
import time
import subprocess

import psutil as psutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import winreg

# Kill any running Chrome processes
os.system("taskkill /im chrome.exe /f")
os.system("taskkill /im chromedriver.exe /f")
time.sleep(5)  # Wait for Chrome to close

def set_chrome_startup_policy():
    reg_path = r"SOFTWARE\Policies\Google\Chrome"
    try:
        key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "RestoreOnStartup", 0, winreg.REG_DWORD, 4)
        try:
            winreg.DeleteKey(key, "RestoreOnStartupURLs")
        except FileNotFoundError:
            pass
        winreg.CloseKey(key)
        print("Chrome startup policy set successfully.")
    except PermissionError:
        print("Permission denied: Please run this script as administrator.")
    except Exception as e:
        print(f"Failed to set policy: {e}")

set_chrome_startup_policy()

# Path to your existing Chrome user data (with Browsec installed)
USER_DATA_DIR = r"C:\Users\alexe\AppData\Local\Google\Chrome\User Data"
PROFILE_DIR = "Default" # "Profile1" #
profile_path = os.path.join(USER_DATA_DIR, PROFILE_DIR)
if not os.path.exists(profile_path):
    os.makedirs(profile_path)

user_data_dir_lower = profile_path.lower()
def find_processes_using_path(target_path):
    locking_processes = []

    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            open_files = proc.info['open_files']
            if open_files:
                for f in open_files:
                    if f.path.lower().startswith(target_path.lower()):
                        locking_processes.append((proc.info['name'], proc.info['pid']))
                        break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return locking_processes

# Run and print
locked = find_processes_using_path(USER_DATA_DIR)
if locked:
    for name, pid in locked:
        print(f"Process: {name}, PID: {pid}")
else:
    print("No processes are locking the path (or not visible via psutil).")

start_url = "https://www.linkedin.com" #@
chrome_options = Options()
chrome_options.binary_location = f"C:/Program Files/Google/Chrome/Application/chrome.exe"
chrome_options.add_argument("--remote-debugging-port=9224")
chrome_options.add_argument("--start-maximized")

"""
chrome_options.add_argument(f'--user-data-dir={USER_DATA_DIR}')
chrome_options.add_argument(f'--profile-directory={PROFILE_DIR}')

chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-session-crashed-bubble")
chrome_options.add_argument("--disable-features=InfiniteSessionRestore")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
"""
print("Installing driver")
latest_release_url = 'https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.4/win64/chromedriver-win64.zip'
driver_path = "C:/chromedriver/chromedriver-win64/chromedriver.exe"
#driver_path = ChromeDriverManager().install()

"""
# Print ChromeDriver version
try:
    driver_version_output = subprocess.run([driver_path, "--version"], capture_output=True, text=True)
    print("ChromeDriver version:", driver_version_output.stdout.strip())
except Exception as e:
    print("Failed to get ChromeDriver version:", e)
"""

# Start Chrome using ChromeDriverManager to avoid version mismatch
print('driver_path: ', driver_path)
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

print("Installed driver")

"""
# Get and print Chrome browser version from user agent
try:
    driver.get("chrome://version")
    chrome_version = driver.execute_script("return navigator.userAgent;")
    print("Chrome version (from user agent):", chrome_version)
except Exception as e:
    print("Failed to get Chrome version:", e)
"""
# Wait for Browsec to auto-connect
driver.get("https://www.google.com")
print("Opened URL:", driver.current_url)
time.sleep(8)

# Go to LinkedIn
#driver.get("https://www.linkedin.com")
#print("Opened URL:", driver.current_url)
#time.sleep(5)

# Save page content
html_content = driver.execute_script("return document.documentElement.innerHTML;")
print(html_content[:1000])
with open("linkedin_page.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Optional: driver.quit()
