# Smart Glasses Project

This project aims to support visually impaired individuals by providing a smart glasses system that enhances mobility and environmental awareness. The system is based on a Raspberry Pi 5 and uses distance sensing to trigger visual and audio alerts.

## Features

- **Directional object detection** with servo-mounted ultrasonic sensor
- **Multi-directional alerts** with unique beep patterns for each direction
- **Dual operation modes**:
  - Automatic scanning: continuously scans the environment
  - Manual mode: provides focused detection in a single direction
- **Button control interface** with short/long press functionality
- **Database logging** of measurements and system events
- **Real-time dashboard** showing recent measurements and statistics

## Hardware Requirements

- Raspberry Pi
- HC-SR04 ultrasonic sensor
- SG90 servo motor
- LED and status LED
- Buzzer
- Push button
- Jumper wires

## Installation

1. Install required Python libraries:
   ```bash
   sudo apt update
   sudo apt install python3-rpi.gpio

## File Structure

- Measurement records are stored at:  
  `/home/ceren/Proje/records/measurements.db`
  
## Project Structure
smart-glasses-for-blind/
├── main.py                     # Main entry point
├── config.py                   # System configuration
├── requirements.txt            # Required libraries
├── hardware/                   # Hardware interface modules
│   ├── __init__.py
│   ├── gpio_controller.py      # GPIO pin management
│   ├── servo_motor.py          # Servo motor control
│   ├── ultrasonic.py           # Ultrasonic sensor functions
│   └── buzzer_led.py           # Audio and visual feedback
├── core/                       # Core functionality
│   ├── __init__.py
│   ├── scanner.py              # Main scanning system
│   ├── direction.py            # Direction detection
│   └── button_handler.py       # Button input processing
└── database/                   # Data storage
    ├── __init__.py
    └── db_manager.py           # Database operations
    ├── __init__.py
    └── db_manager.py       # Database operations
