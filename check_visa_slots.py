import requests
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuration from environment variables
API_KEY = os.environ.get('VISA_API_KEY')
EMAIL_FROM = os.environ.get('EMAIL_FROM')
EMAIL_TO = os.environ.get('EMAIL_TO')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))

# Target location
TARGET_LOCATION = "ABU DHABI"
STATE_FILE = "last_state.json"

def fetch_visa_slots():
    """Fetch visa slot data from the API"""
    url = "https://app.checkvisaslots.com/slots/v3"
    headers = {
        "x-api-key": API_KEY,
        "accept": "*/*",
        "origin": "chrome-extension://beepaenfejnphdgnkmccjcfiieihhogl",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching visa slots: {e}")
        return None

def find_abu_dhabi_slots(data):
    """Extract Abu Dhabi slot information from the response"""
    if not data or 'slotDetails' not in data:
        return None
    
    for location in data['slotDetails']:
        # Check if this is Abu Dhabi (case insensitive match)
        location_name = location.get('location', '').upper()
        if TARGET_LOCATION in location_name:
            return {
                'location': location.get('location'),
                'slots': location.get('slots', 0),
                'start_date': location.get('start_date'),
                'checked': location.get('createdon')
            }
    
    return None

def load_last_state():
    """Load the last known state from file"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading state: {e}")
    return None

def save_state(state):
    """Save current state to file"""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Error saving state: {e}")

def send_email(subject, body):
    """Send email notification"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent successfully to {EMAIL_TO}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def main():
    print(f"Checking visa slots at {datetime.now()}")
    
    # Fetch current data
    data = fetch_visa_slots()
    if not data:
        print("Failed to fetch data")
        return
    
    # Extract Abu Dhabi information
    current_state = find_abu_dhabi_slots(data)
    if not current_state:
        print(f"Could not find {TARGET_LOCATION} in response")
        return
    
    print(f"Current slots for {TARGET_LOCATION}: {current_state['slots']}")
    
    # Load previous state
    last_state = load_last_state()
    
    # Check if slots have opened up
    slots_opened = False
    if last_state:
        last_slots = last_state.get('slots', 0)
        current_slots = current_state['slots']
        
        # Alert if slots went from 0 to positive, or if more slots appeared
        if last_slots == 0 and current_slots > 0:
            slots_opened = True
            print(f"🎉 SLOTS OPENED! {TARGET_LOCATION} now has {current_slots} slots!")
        elif current_slots > last_slots and current_slots > 0:
            slots_opened = True
            print(f"📈 More slots available! Went from {last_slots} to {current_slots}")
    else:
        print("First run - establishing baseline")
        if current_state['slots'] > 0:
            print(f"Note: {current_state['slots']} slots currently available")
    
    # Send notifications if slots opened
    if slots_opened:
        start_date = current_state.get('start_date', 'Unknown')
        subject = f"🎉 Visa Slots Available in {TARGET_LOCATION}!"
        body = f"""Great news!

Visa appointment slots have opened up in {TARGET_LOCATION}!

Number of slots: {current_state['slots']}
Earliest date: {start_date}
Checked at: {datetime.now()}

Go book your appointment now: https://checkvisaslots.com/latest-us-visa-availability/b1b2-regular/

Good luck!
"""
        
        # Send email notification
        send_email(subject, body)
    
    # Save current state
    current_state['last_checked'] = datetime.now().isoformat()
    save_state(current_state)
    
    print("Check complete")

if __name__ == "__main__":
    main()
