# Smart Glasses for Blind Project

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

* Measurement records are stored at:
  `/home/ceren/Proje/records/measurements.db`

## Project Structure

```bash
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
```

## Database

You can access and query the database using the SQLite3 command line interface:

### Open the database

```bash
sqlite3 /home/ceren/Proje/records/measurements.db
```

### Common Commands

```sql
-- List all tables
.tables

-- Show table schema
.schema measurements

-- Show column headers
.headers on

-- Format output as columns
.mode column

-- Show last 10 measurements
SELECT * FROM measurements ORDER BY id DESC LIMIT 10;

-- Show only alarm-triggered measurements
SELECT date_time, distance, angle, direction 
FROM measurements 
WHERE alert_status = 1 
ORDER BY date_time DESC;

-- Count alarms by direction
SELECT direction, COUNT(*) as alarm_count 
FROM measurements 
WHERE alert_status = 1 
GROUP BY direction 
ORDER BY alarm_count DESC;

-- Daily statistics
SELECT 
    DATE(date_time) as date,
    COUNT(*) as total_measurements,
    COUNT(CASE WHEN alert_status = 1 THEN 1 END) as alerts,
    AVG(distance) as avg_distance
FROM measurements 
GROUP BY DATE(date_time) 
ORDER BY date DESC;

-- Exit the SQLite shell
.quit

