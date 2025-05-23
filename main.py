#!/usr/bin/env python3
"""
Main execution file - Object Detection System
"""

import time
import sys
import os

# Add module paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our own modules
from hardware.gpio_controller import GPIOController
from hardware.servo_motor import ServoMotor
from hardware.ultrasonic import UltrasonicSensor
from hardware.buzzer_led import BuzzerLED
from database.db_manager import DatabaseManager
from core.direction import DirectionDetector
from core.button_handler import ButtonHandler
from core.scanner import Scanner
from config import SYSTEM

class ObjectDetectionSystem:
    def __init__(self):
        self.gpio = None
        self.servo = None
        self.ultrasonic = None
        self.buzzer_led = None
        self.db = None
        self.direction = None
        self.button_handler = None
        self.scanner = None
        self.initialized = False
    
    def initialize(self):
        """System initialization"""
        print("Initializing Object Detection System...")
        
        try:
            # Hardware components
            self.gpio = GPIOController()
            if not self.gpio.initialized:
                raise Exception("GPIO initialization failed")
            
            self.servo = ServoMotor(self.gpio)
            self.ultrasonic = UltrasonicSensor(self.gpio)
            self.buzzer_led = BuzzerLED(self.gpio)
            
            # Database
            self.db = DatabaseManager()
            
            # Core components
            self.direction = DirectionDetector()
            self.button_handler = ButtonHandler(self.gpio, self.buzzer_led)
            self.scanner = Scanner(self.servo, self.ultrasonic, self.buzzer_led, 
                                 self.direction, self.db)
            
            # Setup button interrupt
            if not self.button_handler.setup_interrupt():
                print("Warning: Button interrupt setup failed")
            
            self.initialized = True
            print("System initialization completed successfully")
            return True
            
        except Exception as e:
            print(f"Initialization error: {e}")
            return False
    
    def show_system_info(self):
        """Show system information"""
        from config import PINS, SERVO, DISTANCE, DIRECTION
        
        print("=" * 70)
        print("SMART GLASSES FOR BLIND SYSTEM")
        print("=" * 70)
        print(f"Detection Range: {DISTANCE['THRESHOLD']}cm threshold")
        print(f"Servo Range: {SERVO['MIN_ANGLE']}° to {SERVO['MAX_ANGLE']}°")
        print(f"Step Size: {SERVO['STEP']}° per movement")
        print(f"Control Button: GPIO{PINS['BUTTON']}")
        print("Direction Zones:")
        
        for zone_name, zone_info in DIRECTION['ZONES'].items():
            print(f"   • {zone_name} ({zone_info['min']}-{zone_info['max']}°): "
                  f"{len(DIRECTION['BEEP_PATTERNS'][zone_info['code']])} beeps")
        
        print("\nControls:")
        print("   • Short Press: Start/Stop system")
        print("   • Long Press (2s): Toggle Auto/Manual mode")
        print("=" * 70)
    
    def startup_sequence(self):
        """Startup sequence"""
        # Servo to center position
        self.servo.move_to_center()
        time.sleep(SYSTEM['STARTUP_DELAY'])
        
        # Sound and light show
        self.buzzer_led.startup_sequence()
        
        print("System ready! Press button to start scanning...")
        print("Status: STANDBY (Press button to begin)")
    
    def main_loop(self):
        """Main operation loop"""
        print("System initialized. Waiting for user input...")
        
        try:
            while True:
                state = self.button_handler.get_system_state()
                
                if not state['running']:
                    # System pause state
                    self.buzzer_led.status_blink(False)
                    time.sleep(0.8)
                    continue
                
                if state['auto_mode']:
                    # Automatic scanning mode
                    self.scanner.auto_scan_mode(self.button_handler)
                else:
                    # Manual mode
                    self.scanner.manual_mode(self.button_handler)
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nShutdown initiated by user...")
            self.shutdown()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.shutdown()
    
    def shutdown(self):
        """System shutdown"""
        print("Shutting down system...")
        
        # Servo to center position
        if self.servo:
            self.servo.move_to_center()
            time.sleep(1)
        
        # Final database operations
        if self.db:
            self.db.log_system_event("SYSTEM_SHUTDOWN", "System shutdown by user", "MANUAL")
            self.scanner._show_dashboard()  # Final dashboard
        
        # Shutdown sequence
        if self.buzzer_led:
            self.buzzer_led.shutdown_sequence()
        
        # Clean up interrupt
        if self.button_handler:
            self.button_handler.remove_interrupt()
        
        # Clean up hardware
        if self.servo:
            self.servo.stop()
        
        if self.buzzer_led:
            self.buzzer_led.all_off()
        
        if self.gpio:
            self.gpio.cleanup()
        
        print("System shutdown complete!")
    
    def run(self):
        """Main execution function"""
        if not self.initialize():
            print("Failed to initialize system. Exiting...")
            return False
        
        # Show system information
        self.show_system_info()
        
        # Startup sequence
        self.startup_sequence()
        
        # Log system start in system log
        self.db.log_system_event("SYSTEM_START", "Object detection system started", "AUTO")
        
        # Main loop
        self.main_loop()
        
        return True

def main():
    """Main function"""
    try:
        system = ObjectDetectionSystem()
        system.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()