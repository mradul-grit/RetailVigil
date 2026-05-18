# Project: RetailVigil Prototype
# Lead Dev: Mradul Tripathi
import cv2
import ollama
import time
from ultralytics import YOLO
import requests

# --- CONFIGURATION ---
TOKEN = "8235894385:AAFwVWoR_o9eo_Zh2WQXUrwwko0AiA1oKp4"

# 📱 Your Chat ID (this is correct from your screenshot)
CHAT_ID = "7159713524"
COOLDOWN_TIME = 15 # Wait 15 seconds between analyzing frames to avoid spam

# --- HELPER FUNCTIONS ---
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

def analyze_scene_with_vlm(image_path):
    print("🧠 Asking Moondream to analyze the scene...")
    response = ollama.chat(
        model='moondream',
        messages=[{
            'role': 'user',
            'content': 'Briefly describe what the person in this image is doing. Are they hiding something, reaching into a bag, or acting suspiciously?',
            'images': [image_path]
        }]
    )
    return response['message']['content']

# --- MAIN SYSTEM ---
def main():
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0)
    last_analysis_time = 0

    print("🚀 RetailVigil is active. Watching feed...")

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        # 1. Run Object Detection (Fast)
        results = model(frame, classes=[0], verbose=False)
        annotated_frame = results[0].plot()
        cv2.imshow("RetailVigil Dashboard", annotated_frame)

        # 2. Logic: If a person is detected, and we aren't in cooldown...
        if len(results[0].boxes) > 0:
            current_time = time.time()
            if current_time - last_analysis_time > COOLDOWN_TIME:
                print("👀 Person detected! Capturing frame...")
                
                # Save the frame temporarily
                temp_image_path = "temp_capture.jpg"
                cv2.imwrite(temp_image_path, frame)
                
                # 3. Ask the VLM (Reasoning)
                description = analyze_scene_with_vlm(temp_image_path)
                print(f"📝 VLM Analysis: {description}")

                # 4. Agentic Logic (Simple keyword trigger for prototype)
                suspicious_keywords = ['bag', 'hiding', 'pocket', 'stealing', 'reaching']
                if any(word in description.lower() for word in suspicious_keywords):
                    print("🚨 SUSPICIOUS ACTIVITY DETECTED! Sending Alert.")
                    send_telegram_alert(f"🚨 RetailVigil Alert!\n\nSuspicious activity detected:\n{description}")
                else:
                    print("✅ Scene looks normal.")

                last_analysis_time = current_time # Reset cooldown

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()