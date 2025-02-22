from flask import Flask, render_template, Response, jsonify
import threading
import cv2
import torch
from ultralytics import YOLO
from playsound import playsound
import time
from twilio.rest import Client
import serial
import mysql.connector  # MySQL Integration
import random  # Simulating GPS coordinates
import os

app = Flask(__name__)

# Create a folder for storing drone images
IMAGE_FOLDER = "static/drone_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sanu#718",
    database="dronedb"
)
cursor = db.cursor()

# Ensure table exists with new columns
cursor.execute("""
    CREATE TABLE IF NOT EXISTS drone_detections (
        id INT AUTO_INCREMENT PRIMARY KEY,
        detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        latitude DECIMAL(9,6),
        longitude DECIMAL(9,6),
        image_path VARCHAR(255)
    )
""")
db.commit()

# Global variables
drone_detected = False
detection_start_time = None
detection_duration = 5

# Load YOLO model
model = YOLO("C:\\Users\\satya\\Documents\\dronetrack\\runs\\detect\\train2\\weights\\best.pt")

# Initialize Serial Communication
try:
    arduino = serial.Serial('COM8', 9600, timeout=1)
    time.sleep(5)
    print("✅ Arduino connected successfully!")
except Exception as e:
    print(f"❌ Error connecting to Arduino: {e}")
    arduino = None

# Function to play siren
def play_siren():
    playsound("C:/dronetrack/war.mp3")

# Function to send SMS alert
def send_sms():
    try:
        client = Client("TWILIO_SID", "TWILIO_AUTH_TOKEN")
        client.messages.create(
            body="🚨 ALERT: DRONE DETECTED! 🚨 Take necessary precautions!",
            from_="+18125754276",
            to="+918260515912"
        )
    except Exception as e:
        print(f"❌ Error sending SMS: {str(e)}")

# Function to log detection in MySQL with GPS & Image
def log_detection(latitude, longitude, frame):
    timestamp = time.strftime("%Y%m%d%H%M%S")
    image_path = f"{IMAGE_FOLDER}/drone_{timestamp}.jpg"
    
    # Save image to disk
    cv2.imwrite(image_path, frame)
    
    # Insert into MySQL
    cursor.execute(
        "INSERT INTO drone_detections (detected_at, latitude, longitude, image_path) VALUES (NOW(), %s, %s, %s)",
        (latitude, longitude, image_path)
    )
    db.commit()
    print("✅ Detection logged with GPS & Image.")

# Video Capture
cap = cv2.VideoCapture(0)

# Function to process video frames
def generate_frames():
    global drone_detected, detection_start_time

    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model.predict(frame)
        detected = any(
            model.names[int(box.cls[0].item())].lower() == "drone"
            for result in results for box in result.boxes
        )

        if detected:
            if detection_start_time is None:
                detection_start_time = time.time()
            elif time.time() - detection_start_time >= detection_duration and not drone_detected:
                print("🚀 Drone detected for 5 seconds! Triggering alerts.")
                
                # Simulating GPS coordinates (Replace with actual GPS sensor input)
                latitude = round(random.uniform(37.0, 38.0), 6)
                longitude = round(random.uniform(-122.0, -121.0), 6)

                threading.Thread(target=play_siren, daemon=True).start()
                threading.Thread(target=send_sms, daemon=True).start()
                if arduino:
                    arduino.write(b'FIRE\n')
                
                log_detection(latitude, longitude, frame)  # Log detection with GPS & Image

                drone_detected = True
        else:
            detection_start_time = None
            drone_detected = False

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               buffer.tobytes() +
               b'\r\n')

# Flask Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/drone_status')
def drone_status():
    return jsonify({"drone_detected": drone_detected})

# **Updated Route for Viewing Logs (with GPS & Image)**
@app.route('/drone_database')
def drone_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sanu#718",
        database="dronedb"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT detected_at, latitude, longitude, image_path FROM drone_detections ORDER BY detected_at DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('logs.html', detections=data)

# **New Route for JSON Logs**
@app.route('/drone_database_json')
def drone_database_json():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sanu#718",
        database="dronedb"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT detected_at, latitude, longitude, image_path FROM drone_detections ORDER BY detected_at DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

# Run Flask App
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
