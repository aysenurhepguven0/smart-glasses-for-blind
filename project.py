import RPi.GPIO as GPIO
import time
import datetime
import sqlite3
import os
from pathlib import Path

# Pin definitions
TRIG_PIN = 23      # Ultrasonic sensor trigger pin (GPIO23)
ECHO_PIN = 24      # Ultrasonic sensor echo pin (GPIO24)
LED_PIN = 18       # LED pin (GPIO18)
BUZZER_PIN = 26    # Buzzer pin(GPIO26)

# Distance threshold 
THRESHOLD = 100    # 1 meter (100 cm)

# SQLite database settings
RECORDS_FOLDER = "/home/ceren/Proje/records"
DB_FILE = os.path.join(RECORDS_FOLDER, "measurements.db")

def play_startup_melody():
    print("Playing startup melody...")
    
    # Define the notes of the melody
    # Each tuple contains (duration, pause)
    notes = [
        (0.1, 0.05),  # C
        (0.1, 0.05),  # E
        (0.1, 0.05),  # G
        (0.3, 0.1),   # C (higher, longer)
    ]
    
    # LED feedback during startup
    for i in range(3):
        GPIO.output(LED_PIN, True)
        time.sleep(0.1)
        GPIO.output(LED_PIN, False)
        time.sleep(0.1)
    
    # Play the melody
    for duration, pause in notes:
        GPIO.output(LED_PIN, True)      # Visual feedback with LED
        GPIO.output(BUZZER_PIN, True)   # Sound the buzzer
        time.sleep(duration)            # Note duration
        
        GPIO.output(BUZZER_PIN, False)  # Stop the buzzer
        time.sleep(pause)               # Pause between notes
    
    GPIO.output(LED_PIN, True)
    time.sleep(0.5)
    GPIO.output(LED_PIN, False)
    
    print("System initialized!")

def play_shutdown_melody():
    """Play a shutdown melody like Windows shutdown sound"""
    print("Playing shutdown melody...")
    
    # Define the notes of the shutdown melody
    # Each tuple contains (duration, pause)
    # Reverse pattern from startup - high to low
    notes = [
        (0.3, 0.1),   # C (higher, longer)
        (0.1, 0.05),  # G
        (0.1, 0.05),  # E
        (0.1, 0.05),  # C (lower)
    ]
    
    # Play the shutdown melody
    for duration, pause in notes:
        GPIO.output(LED_PIN, True)      # Visual feedback with LED
        GPIO.output(BUZZER_PIN, True)   # Sound the buzzer
        time.sleep(duration)            # Note duration
        
        GPIO.output(BUZZER_PIN, False)  # Stop the buzzer
        GPIO.output(LED_PIN, False)     # Turn off LED
        time.sleep(pause)               # Pause between notes
    
    # Final signoff - three quick LED flashes
    for i in range(3):
        GPIO.output(LED_PIN, True)
        time.sleep(0.05)
        GPIO.output(LED_PIN, False)
        time.sleep(0.05)

def create_records_folder():
    """Create the records folder"""
    Path(RECORDS_FOLDER).mkdir(parents=True, exist_ok=True)
    print(f"Records will be stored in '{RECORDS_FOLDER}' folder")

def create_database():
    """Create SQLite database and table"""
    try:
        # First create the folder
        create_records_folder()
        
        # Establish database connection
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Create measurements table (if it doesn't exist)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TEXT NOT NULL,
            distance REAL NOT NULL,
            alert_status INTEGER NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
        print(f"SQLite database '{DB_FILE}' successfully created")
        return True
    except Exception as e:
        print(f"Database creation error: {e}")
        return False

def establish_database_connection():
    """Establish SQLite connection and return connection object"""
    try:
        conn = sqlite3.connect(DB_FILE)
        print("SQLite database connection successful")
        return conn
    except Exception as e:
        print(f"SQLite connection error: {e}")
        return None

def save_to_database(conn, date_time, distance, alert_status):
    """Save measurement results to SQLite database"""
    if conn:
        try:
            cursor = conn.cursor()
            
            # Add data
            cursor.execute(
                "INSERT INTO measurements (date_time, distance, alert_status) VALUES (?, ?, ?)",
                (date_time.strftime('%Y-%m-%d %H:%M:%S'), distance, alert_status)
            )
            
            conn.commit()
            print(f"Data saved: {date_time}, {distance} cm, Alert: {alert_status}")
        except Exception as e:
            print(f"Data saving error: {e}")

def show_table_data(conn):
    """Fetch and display recent data from database"""
    if conn:
        try:
            cursor = conn.cursor()
            
            # Get last 10 records
            cursor.execute("""
            SELECT id, date_time, distance, alert_status
            FROM measurements
            ORDER BY id DESC
            LIMIT 10
            """)
            
            rows = cursor.fetchall()
            
            print("\n" + "="*60)
            print("DATABASE RECORDS (Last 10 entries)")
            print("="*60)
            print(f"{'ID':<5} {'Date/Time':<20} {'Distance (cm)':<15} {'Alert'}")
            print("-"*60)
            
            for row in rows:
                id, date_time, distance, alert = row
                print(f"{id:<5} {date_time:<20} {distance:<15.2f} {'YES' if alert else 'NO'}")
            
            print("="*60)
            
            # Show statistics
            cursor.execute("SELECT COUNT(*) FROM measurements")
            total_records = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM measurements WHERE alert_status = 1")
            alert_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(distance) FROM measurements")
            avg_distance = cursor.fetchone()[0] or 0
            
            print(f"Total Records: {total_records}, Alert Count: {alert_count}, Average Distance: {avg_distance:.2f} cm")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"Data display error: {e}")

def setup():
    """Initialize GPIO settings"""
    # Set GPIO mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Set pin modes
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    
    # Initialize all outputs to low
    GPIO.output(TRIG_PIN, False)
    GPIO.output(LED_PIN, False)
    GPIO.output(BUZZER_PIN, False)
    
    print("Ultrasonic Sensor, LED and Buzzer Test Program")
    print(f"Threshold value: {THRESHOLD} cm")
    print("System starting...")
    
    # Play the startup melody
    play_startup_melody()
    
    print("System ready!")

def measure_distance():
    """Measure distance with ultrasonic sensor"""
    # Trigger the ultrasonic sensor
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG_PIN, False)
    
    start_time = time.time()
    end_time = time.time()
    
    # Update start time until Echo pin goes LOW
    timeout_start = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
        # Timeout check
        if time.time() - timeout_start > 1:
            return -1
    
    # Update end time until Echo pin goes HIGH
    while GPIO.input(ECHO_PIN) == 1:
        end_time = time.time()
        # Timeout check
        if end_time - start_time > 1:
            return -1
    
    # Calculate sound wave round-trip time
    duration = end_time - start_time
    
    # Calculate distance in cm (sound speed = 34300 cm/s)
    # Divide by 2 for round-trip
    distance = (duration * 34300) / 2
    
    return distance

def main():
    try:
        # Initialize GPIO settings
        setup()
        
        # Create SQLite database (if it doesn't exist)
        create_database()
        
        # Establish SQLite connection
        conn = establish_database_connection()
        
        measurement_count = 0  # Measurement counter
        
        # Main program loop
        while True:
            # Get current date and time
            now = datetime.datetime.now()
            
            # Distance measurement
            distance = measure_distance()
            
            # Process if valid distance value
            if distance > 0:
                measurement_count += 1  # Increment measurement counter
                distance_rounded = round(distance, 2)
                print(f"Distance: {distance_rounded} cm (Measurement #{measurement_count})")
                
                # Is distance less than threshold?
                alert_status = 0  # 0: No alert, 1: Alert
                
                if distance < THRESHOLD:
                    # Turn on LED
                    GPIO.output(LED_PIN, True)
                    
                    # Sound buzzer for 1 second
                    GPIO.output(BUZZER_PIN, True)
                    print("LED and Buzzer: ON")
                    alert_status = 1
                    
                    # Save to SQLite
                    if conn:
                        save_to_database(conn, now, distance_rounded, alert_status)
                    
                    time.sleep(1)
                    GPIO.output(BUZZER_PIN, False)  # Turn off buzzer
                    time.sleep(0.5)  # Wait 0.5 seconds
                else:
                    # Distance greater than threshold - LED and buzzer off
                    GPIO.output(LED_PIN, False)
                    GPIO.output(BUZZER_PIN, False)
                    print("LED and Buzzer: OFF")
                
                # Display table data every 30 measurements
                if measurement_count % 30 == 0 and conn:
                    show_table_data(conn)
            else:
                print("Distance measurement failed. Check sensor connections.")
            
            # Short delay between measurements
            time.sleep(0.2)
            
    except KeyboardInterrupt:
        # When program is terminated with Ctrl+C
        print("\nProgram termination requested...")
        play_shutdown_melody()
        print("Program terminated.")
    except Exception as e:
        # Other errors
        print(f"Unexpected error: {e}")
    finally:
        # Close connection
        if 'conn' in locals() and conn:
            conn.close()
            print("Database connection closed.")
        
        # Clean up pins
        GPIO.cleanup()
        print("GPIO pins cleaned up.")

if __name__ == "__main__":
    main()