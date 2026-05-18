"""
RetailVigil camera/vision entry module.
"""

# Author: Mradul Tripathi
import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO('yolov8n.pt')

# Open webcam (Windows fix included)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 🔍 Check if camera opened
if not cap.isOpened():
    print("❌ Camera failed to open")
    exit()
else:
    print("✅ Camera opened successfully")

print("Press 'q' in the video window to quit!")

# Create window properly
cv2.namedWindow("RetailVigil - Eyes Test", cv2.WINDOW_NORMAL)

# Main loop
while True:
    success, frame = cap.read()

    if not success:
        print("❌ Failed to read frame")
        break

    # Run YOLO detection (person only)
    results = model(frame, classes=[0], verbose=False)

    # Draw boxes
    annotated_frame = results[0].plot()

    # Show output
    cv2.imshow("RetailVigil - Eyes Test", annotated_frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()