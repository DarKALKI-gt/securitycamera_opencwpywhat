import cv2
import numpy as np
import time
import os
import pywhatkit
import requests 


TARGET_OBJECT = "laptop"

PHONE_NUMBER = "+917524hello"
CONFIDENCE_THRESHOLD = 0.5 
SEND_COOLDOWN = 60 


def get_location():
    """
    Fetches the approximate location and a Google Maps link using the public IP address.
    """
    try:
       
        response = requests.get('https://ipinfo.io/json', timeout=5).json()
        city = response.get('city', 'Unknown City')
        region = response.get('region', 'Unknown Region')
        country = response.get('country', 'IN')
        lat, lon = response.get('loc', '0,0').split(',')
        
        
        location_str = f"{city}, {region}, {country}"
        map_link = f"https://www.google.com/maps?q={lat},{lon}"
        
        return location_str, map_link
    except Exception as e:
        print(f"Error: Could not fetch location. {e}")
        return "Location unavailable", None


def send_whatsapp_alert(phone_num, img_path, detected_label):
    """
    Sends a formatted alert with snapshot, location, and map link to WhatsApp.
    """
    try:
        location_str, map_link = get_location()
        current_time_str = time.strftime("%Y-%m-%d %H:%M:%S")

       
        caption = (
            f"🚨 Security Alert! 🚨\n\n"
            f"Object Detected: *{detected_label.capitalize()}*\n"
            f"Time: {current_time_str}\n"
            f"Approx. Location: {location_str}"
        )

        
        pywhatkit.sendwhats_image(phone_num, img_path, caption, wait_time=20, tab_close=True)
        print(f"✅ Successfully sent snapshot to {phone_num}")
        
        time.sleep(10) 

        
        if map_link:
            pywhatkit.sendwhatmsg_instantly(phone_num, f"View on map: {map_link}", wait_time=15, tab_close=True)
            print(f"✅ Sent location link separately.")

        time.sleep(5)
        os.remove(img_path)
        print(f"Removed temporary file: {img_path}")

    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {e}")


print("Loading YOLO model...")
try:
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    
    layer_names = net.getLayerNames()
    output_layers_indices = net.getUnconnectedOutLayers()
    if isinstance(output_layers_indices, tuple) or (output_layers_indices.ndim > 1):
        output_layers_indices = output_layers_indices.flatten()
    output_layers = [layer_names[i - 1] for i in output_layers_indices]
    print("YOLO model loaded successfully.")
except FileNotFoundError:
    print("❌ Error: YOLO model files not found! Make sure 'yolov3.weights', 'yolov3.cfg', and 'coco.names' are in the same folder as the script.")
    exit()

# --- Initialize Webcam ---
print("Starting webcam...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

last_send_time = 0


try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > CONFIDENCE_THRESHOLD:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, 0.4)
        
        detected_target_in_frame = False
        if len(indexes) > 0:
            for i in indexes.flatten():
                label = str(classes[class_ids[i]])
                x, y, w, h = boxes[i]
                
                
                if label == TARGET_OBJECT:
                    detected_target_in_frame = True
                    color = (0, 0, 255) 
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, f"**{label.upper()}**", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                else:
                    color = (0, 255, 0)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

       
        current_time = time.time()
        if detected_target_in_frame and (current_time - last_send_time > SEND_COOLDOWN):
            print(f"‼️  {TARGET_OBJECT.capitalize()} detected! Preparing to send alert...")
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            snapshot_path = f"detection_{timestamp}.jpg"
            cv2.imwrite(snapshot_path, frame)
            
            send_whatsapp_alert(PHONE_NUMBER, snapshot_path, TARGET_OBJECT)
            
            last_send_time = current_time

        cv2.imshow("Security Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    print("Closing script...")
    cap.release()

    cv2.destroyAllWindows()
