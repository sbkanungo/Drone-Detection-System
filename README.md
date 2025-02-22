# Drone Detection System

## Overview
The **Drone Detection System** is a real-time drone monitoring and alerting system built using **Flask, OpenCV, YOLO, MySQL, and Arduino**. It detects unauthorized drones, triggers alerts, and logs detection details.

## Features
- **Drone Detection**: Uses **YOLO (You Only Look Once)** and **OpenCV** for real-time object detection.
- **Live Streaming**: Flask web application displays live detection feed.
- **Alert Mechanism**: Plays a siren and sends an SMS alert via Twilio upon detection.
- **Database Logging**: Stores detection logs, including drone images, timestamps, GPS coordinates in **MySQL**.
- **Arduino Integration**: Communicates with Arduino to trigger external alarms or countermeasures.
- **Remote Database Access**: MySQL database is accessible remotely for multi-system integration.

## Tech Stack
- **Frontend**: Flask Web App
- **Backend**: Python (Flask, OpenCV, YOLO)
- **Database**: MySQL
- **Hardware**: Arduino (for alarm triggering), Camera for detection
- **Messaging**: Twilio (for SMS alerts)

## Installation & Setup
### Prerequisites
- Python 3.x
- MySQL Server
- Arduino IDE (if using Arduino)
- Flask & Required Python Libraries

### 1. Clone the Repository
```sh
git clone https://github.com/sbkanungo/Drone-Detection-System.git
cd Drone-Detection-System
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Set Up MySQL Database
1. Start MySQL Server.
2. Create a database and update `config.py` with your database credentials.
3. Run the following SQL script to create necessary tables:
```sql
CREATE DATABASE drone_detection;
USE drone_detection;
CREATE TABLE detections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT,
    image_path VARCHAR(255)
);
```

### 4. Run the Flask Application
```sh
python app.py
```

Access the web interface at: [http://localhost:5000](http://localhost:5000)

### 5. Connecting to MySQL Remotely
If accessing MySQL remotely, ensure your server is listening for external connections and update firewall rules.

## Usage
- The system will detect drones using YOLO and OpenCV.
- If a drone is detected:
  - The system will **trigger an alarm**.
  - A **snapshot** of the drone is saved in the database.
  - **GPS coordinates** are logged in MySQL.
  - An **SMS alert** is sent via Twilio.

## Troubleshooting
- **YOLO Model Not Found?** Ensure the YOLO weight files are in the correct directory.
- **MySQL Connection Issues?** Check `config.py` and ensure MySQL allows remote connections.
- **Flask Not Starting?** Ensure all dependencies are installed correctly.

## Future Enhancements
- Implement AI-based drone classification.
- Add MQTT support for IoT integration.
- Improve GUI for web-based monitoring.


