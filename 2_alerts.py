import requests

# 🔐 Replace with your NEW token (after revoke)
TOKEN = "8235894385:AAFwVWoR_o9eo_Zh2WQXUrwwko0AiA1oKp4"

# 📱 Your Chat ID (this is correct from your screenshot)
CHAT_ID = "7159713524"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, json=payload)

        print("🔍 Status Code:", response.status_code)
        print("🔍 Response:", response.text)

        if response.status_code == 200:
            print("✅ Alert sent successfully!")
        else:
            print("❌ Failed to send alert")

    except Exception as e:
        print("❌ Error occurred:", str(e))


# 🚀 Test message
send_telegram_alert("🚨 RetailVigil Test: System is online.")