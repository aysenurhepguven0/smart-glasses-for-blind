#Servo motor controller
import RPi.GPIO as GPIO
import time
from config import PINS, SERVO

class ServoMotor:
    def __init__(self, gpio_controller):
        self.gpio = gpio_controller
        self.pwm = None
        self.current_angle = 90
        self.setup_servo()
        
    def setup_servo(self):
        try:
            self.pwm = GPIO.PWM(PINS['SERVO'], SERVO['PWM_FREQUENCY'])
            self.pwm.start(0)
            print("Servo motor initialized")
        except Exception as e:
            print(f"Servo initialization error: {e}")
        
    def set_angle(self, angle):
        if not self.pwm:
            return False
            
        # Limit angle to valid range
        angle = max(SERVO['MIN_ANGLE'], min(SERVO['MAX_ANGLE'], angle))
            
        try:
            # Calculate duty cycle (for SG90 servo)
            duty_cycle = 2 + (angle / 180) * 10
                
            self.pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(SERVO['SPEED_DELAY'])
                
            # Stop PWM to reduce servo jitter
            self.pwm.ChangeDutyCycle(0)
                
            self.current_angle = angle
            return True
                
        except Exception as e:
            print(f"Servo angle setting error: {e}")
            return False
        
    def sweep(self, start_angle=None, end_angle=None, step=None):
        """Angle scanning"""
        start_angle = start_angle or SERVO['MIN_ANGLE']
        end_angle = end_angle or SERVO['MAX_ANGLE']
        step = step or SERVO['STEP']
            
        angles = []
            
        # Forward direction
        current = start_angle
        while current <= end_angle:
            angles.append(current)
            current += step
            
        # Backward direction
        current = end_angle - step
        while current >= start_angle:
            angles.append(current)
            current -= step
            
        return angles
        
    def move_to_center(self):
        """Go to center position"""
        center = (SERVO['MIN_ANGLE'] + SERVO['MAX_ANGLE']) // 2
        return self.set_angle(center)
        
    def get_current_angle(self):
        """Return current angle"""
        return self.current_angle
        
    def stop(self):
        """Stop servo motor"""
        if self.pwm:
            try:
                self.pwm.stop()
                print("Servo motor stopped")
            except Exception as e:
                print(f"Servo stop error: {e}")
        
    def __del__(self):
        """Destructor"""
        self.stop()