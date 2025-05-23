#GPIO controller

import RPi.GPIO as GPIO
import time
from config import PINS

class GPIOController:
    def __init__(self):
        self.initialized = False
        self.setup_gpio()
    
    def setup_gpio(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            # Input pins
            GPIO.setup(PINS['ECHO'], GPIO.IN)
            GPIO.setup(PINS['BUTTON'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
            # Output pins
            GPIO.setup(PINS['TRIG'], GPIO.OUT)
            GPIO.setup(PINS['LED'], GPIO.OUT)
            GPIO.setup(PINS['BUZZER'], GPIO.OUT)
            GPIO.setup(PINS['SERVO'], GPIO.OUT)
            GPIO.setup(PINS['STATUS_LED'], GPIO.OUT)
            
            # Initial 
            GPIO.output(PINS['TRIG'], False)
            GPIO.output(PINS['LED'], False)
            GPIO.output(PINS['BUZZER'], False)
            GPIO.output(PINS['STATUS_LED'], False)
            
            self.initialized = True
            print("GPIO pins initialized successfully")
            
        except Exception as e:
            print(f"GPIO initialization error: {e}")
            self.initialized = False
    
    def read_pin(self, pin_name):
        if not self.initialized:
            return None
        try:
            return GPIO.input(PINS[pin_name])
        except Exception as e:
            print(f"Error reading pin {pin_name}: {e}")
            return None
    
    def write_pin(self, pin_name, state):
        if not self.initialized:
            return False
        try:
            GPIO.output(PINS[pin_name], state)
            return True
        except Exception as e:
            print(f"Error writing to pin {pin_name}: {e}")
            return False
    
    def setup_interrupt(self, pin_name, callback, edge=GPIO.FALLING, bouncetime=300):
        if not self.initialized:
            return False
        try:
            GPIO.add_event_detect(PINS[pin_name], edge, callback=callback, bouncetime=bouncetime)
            return True
        except Exception as e:
            print(f"Error setting up interrupt for {pin_name}: {e}")
            return False
    
    def remove_interrupt(self, pin_name):
        try:
            GPIO.remove_event_detect(PINS[pin_name])
        except Exception as e:
            print(f"Error removing interrupt for {pin_name}: {e}")
    
    def cleanup(self):
        if self.initialized:
            try:
                for pin_name in ['LED', 'BUZZER', 'STATUS_LED', 'TRIG']:
                    self.write_pin(pin_name, False)
                
                GPIO.cleanup()
                print("GPIO cleanup completed")
            except Exception as e:
                print(f"GPIO cleanup error: {e}")
    
    def __del__(self):
        """Destructor"""
        self.cleanup()