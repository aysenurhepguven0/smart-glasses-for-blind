"""Configuration file - All system settings """
import os
from pathlib import Path

# GPIO Pin Definitions
PINS = {
    'TRIG': 23,          # Ultrasonic sensor trigger pin (GPIO23)
    'ECHO': 24,          # Ultrasonic sensor echo pin (GPIO24)
    'LED': 18,           # LED pin (GPIO18)
    'BUZZER': 26,        # Buzzer pin (GPIO26)
    'SERVO': 12,         # Servo motor pin (GPIO12)
    'BUTTON': 22,        # Button pin (GPIO22)
    'STATUS_LED': 16     # System status LED pin (GPIO16)
}

# Distance Detection Settings
DISTANCE = {
    'THRESHOLD': 50,      # Alarm distance threshold (cm)
    'MIN_VALID': 2,      # Minimum valid distance (cm)
    'MAX_VALID': 400     # Maximum valid distance (cm)
}

# Servo Motor Settings
SERVO = {
    'MIN_ANGLE': 76,     # Minimum angle
    'MAX_ANGLE': 164,    # Maximum angle
    'STEP': 2,           # Angle step size
    'SPEED_DELAY': 0.1,  # Movement speed delay (seconds)
    'PWM_FREQUENCY': 50  # PWM frequency (Hz)
}

# System Settings
SYSTEM = {
    'MEASUREMENT_INTERVAL': 0.05,  # Measurement interval (seconds)
    'BUTTON_DEBOUNCE': 300,        # Button debounce time (ms)
    'LONG_PRESS_TIME': 2,          # Long press time (seconds)
    'STARTUP_DELAY': 1             # Startup delay (seconds)
}

# Database Settings
DATABASE = {
    'FOLDER': "/home/ceren/Proje/records",
    'FILE': "measurements.db",
    'CONNECTION_TIMEOUT': 10,
    'MAX_RETRIES': 3
}

# Full database path
DB_PATH = os.path.join(DATABASE['FOLDER'], DATABASE['FILE'])

# Direction Detection Settings
DIRECTION = {
    'ZONES': {
        'FAR_LEFT': {'min': 150, 'max': 180, 'code': 4, 'name': 'FAR_LEFT'},
        'LEFT': {'min': 138, 'max': 150, 'code': 2, 'name': 'LEFT'},
        'FRONT': {'min': 124, 'max': 138, 'code': 3, 'name': 'FRONT'},
        'RIGHT': {'min': 100, 'max': 124, 'code': 1, 'name': 'RIGHT'},
        'FAR_RIGHT': {'min': 0, 'max': 90, 'code': 5, 'name': 'FAR_RIGHT'}
    },
    'BEEP_PATTERNS': {
        1: [(0.1, 0.05)],  # RIGHT - 1 short beep
        2: [(0.3, 0.1), (0.3, 0.1)],  # LEFT - 2 long beeps
        3: [(0.15, 0.05), (0.15, 0.05), (0.15, 0.05)],  # FRONT - 3 medium beeps
        4: [(0.05, 0.05)] * 4,  # FAR_LEFT - 4 very short beeps
        5: [(0.05, 0.05)] * 5   # FAR_RIGHT - 5 very short beeps
    }
}

# Audio Settings
AUDIO = {
    'STARTUP_NOTES': [
        (0.1, 0.05),   # C
        (0.1, 0.05),   # E
        (0.1, 0.05),   # G
        (0.2, 0.1),    # C (high)
        (0.3, 0.1),    # C (long)
    ],
    'SHUTDOWN_NOTES': [
        (0.3, 0.1),    # High C
        (0.2, 0.05),   # G
        (0.2, 0.05),   # E
        (0.4, 0.1),    # Low C (long)
    ]
}

# Logging Settings
LOGGING = {
    'LEVEL': 'INFO',
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'FILE': 'system.log'
}

# Display Settings
DISPLAY = {
    'DASHBOARD_WIDTH': 90,
    'RECENT_RECORDS': 8,
    'SEPARATOR': '='
}