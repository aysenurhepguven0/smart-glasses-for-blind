# Smart Glasses Project

This project aims to support visually impaired individuals by providing a smart glasses system that enhances mobility and environmental awareness. The system is based on a Raspberry Pi 5 and uses distance sensing to trigger visual and audio alerts.

## Features

- **Distance measurement** using an HC-SR04 ultrasonic sensor  
- **Alerts via LED and buzzer** when objects are detected closer than a set threshold (100 cm)  
- **SQLite database logging** (timestamp, distance, alert status)  
- **Displays last 10 entries** and statistics every 30 measurements  
- **Startup and shutdown melodies** with LED and buzzer feedback  

## Hardware Requirements

- Raspberry Pi 5  
- HC-SR04 Ultrasonic Sensor  
- LED  
- Buzzer  
- Jumper wires  

## Installation

1. Install required Python libraries:
    ```bash
    sudo apt update
    sudo apt install python3-rpi.gpio
    ```

2. Clone the repository and run the main script:
    ```bash
    python3 main.py
    ```

## File Structure

- Measurement records are stored at:  
  `/home/ceren/Proje/records/measurements.db`

