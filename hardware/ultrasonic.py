# Ultrasonic sensor control 
import time
from config import DISTANCE

class UltrasonicSensor:
    def __init__(self, gpio_controller):
        self.gpio = gpio_controller
        self.last_distance = 0
        
    def measure_distance(self):
        try:
            # Send trigger signal
            self.gpio.write_pin('TRIG', True)
            time.sleep(0.00001)  # 10 microseconds
            self.gpio.write_pin('TRIG', False)
            
            # Wait for echo start
            timeout_start = time.time()
            while self.gpio.read_pin('ECHO') == 0:
                if time.time() - timeout_start > 1:
                    return -1
                start_time = time.time()
                
            # Wait for echo end
            while self.gpio.read_pin('ECHO') == 1:
                end_time = time.time()
                if end_time - start_time > 1:
                    return -1
                
            # Distance calculation
            duration = end_time - start_time
            distance = (duration * 34300) / 2  # Speed of sound: 343 m/s
                
            # Valid range check
            if DISTANCE['MIN_VALID'] <= distance <= DISTANCE['MAX_VALID']:
                self.last_distance = distance
                return round(distance, 2)
            else:
                return -1
                
        except Exception as e:
            print(f"Distance measurement error: {e}")
            return -1
        
    def is_object_detected(self, distance=None):
        if distance is None:
            distance = self.measure_distance()
                
        if distance > 0:
            return distance < DISTANCE['THRESHOLD']
        return False
        
    def get_last_distance(self):
        return self.last_distance
        
    def multiple_measurements(self, count=3):
        """Multiple measurements - for more accurate results"""
        measurements = []
                
        for _ in range(count):
            distance = self.measure_distance()
            if distance > 0:
                measurements.append(distance)
            time.sleep(0.01)  # Short wait
                
        if measurements:
            # Return median value
            measurements.sort()
            mid = len(measurements) // 2
            return measurements[mid]
                
        return -1