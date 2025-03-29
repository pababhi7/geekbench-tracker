import requests
import json
import os

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={'chat_id': CHAT_ID, 'text': text})

def get_devices():
    response = requests.get('https://browser.geekbench.com/v6/cpu/search.json')
    return response.json().get('devices', [])

def main():
    # Load previous devices
    try:
        with open('devices.json') as f:
            old_devices = json.load(f)
    except:
        old_devices = []

    # Get current devices
    new_devices = get_devices()
    
    # Find new entries
    added = [d for d in new_devices if d not in old_devices]
    
    # Send notifications
    if added:
        message = "🚨 New Devices Found:\n" + "\n".join(
            [f"- {d['name']} (ID: {d['id']})" for d in added]
        )
        send_message(message)
    
    # Save new list
    with open('devices.json', 'w') as f:
        json.dump(new_devices, f)
    
    # Send test message if triggered
    if os.environ.get('SEND_TEST') == "true":
        send_message("✅ Test message successful! Monitoring is active.")

if __name__ == "__main__":
    main()
