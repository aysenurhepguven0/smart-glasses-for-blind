#Buzzer and Led Control
import time
from config import AUDIO

class BuzzerLED:
    def __init__(self, gpio_controller):
        self.gpio = gpio_controller
    
    def led_on(self, led_type='LED'):
        return self.gpio.write_pin(led_type, True)
    
    def led_off(self, led_type='LED'):
        return self.gpio.write_pin(led_type, False)
    
    def buzzer_on(self):
        return self.gpio.write_pin('BUZZER', True)
    
    def buzzer_off(self):
        return self.gpio.write_pin('BUZZER', False)
    
    def beep(self, duration=0.1, pause=0.05):
        """Single beep sound"""
        self.buzzer_on()
        time.sleep(duration)
        self.buzzer_off()
        time.sleep(pause)
    
    def beep_pattern(self, pattern):
        """Play beep pattern"""
        for duration, pause in pattern:
            self.beep(duration, pause)
    
    def led_blink(self, led_type='LED', count=1, duration=0.1, pause=0.1):
        for _ in range(count):
            self.led_on(led_type)
            time.sleep(duration)
            self.led_off(led_type)
            time.sleep(pause)
    
    def startup_sequence(self):
        print("Playing startup sequence...")
        
        # LED sequence
        for _ in range(5):
            self.led_blink('STATUS_LED', 1, 0.1, 0.1)
        
        # Music sequence
        for duration, pause in AUDIO['STARTUP_NOTES']:
            self.led_on('STATUS_LED')
            self.buzzer_on()
            time.sleep(duration)
            
            self.buzzer_off()
            self.led_off('STATUS_LED')
            time.sleep(pause)
        
        # Final signal
        self.led_on('STATUS_LED')
        time.sleep(0.5)
        self.led_off('STATUS_LED')
        
        print("Startup sequence completed")
    
    def shutdown_sequence(self):
        print("Playing shutdown sequence...")
        
        for duration, pause in AUDIO['SHUTDOWN_NOTES']:
            self.led_on('STATUS_LED')
            self.buzzer_on()
            time.sleep(duration)
            
            self.buzzer_off()
            self.led_off('STATUS_LED')
            time.sleep(pause)
        
        # Final blinking
        for _ in range(3):
            self.led_blink('STATUS_LED', 1, 0.1, 0.1)
        
        print("Shutdown sequence completed")
    
    def system_start_signal(self):
        for _ in range(2):
            self.led_on('STATUS_LED')
            self.buzzer_on()
            time.sleep(0.15)
            self.led_off('STATUS_LED')
            self.buzzer_off()
            time.sleep(0.1)
    
    def system_pause_signal(self):
        self.led_on('STATUS_LED')
        self.buzzer_on()
        time.sleep(0.5)
        self.led_off('STATUS_LED')
        self.buzzer_off()
    
    def mode_change_signal(self):
        for _ in range(3):
            self.led_on('STATUS_LED')
            self.buzzer_on()
            time.sleep(0.1)
            self.led_off('STATUS_LED')
            self.buzzer_off()
            time.sleep(0.1)
    
    def alert_signal(self, direction_code):
        from config import DIRECTION
        
        pattern = DIRECTION['BEEP_PATTERNS'].get(direction_code, [(0.15, 0.05)])
        
        # LED and buzzer together
        self.led_on('LED')
        self.beep_pattern(pattern)
        self.led_off('LED')
    
    def status_blink(self, active=True):
        if active:
            self.led_blink('STATUS_LED', 1, 0.8, 0.8)
        else:
            self.led_off('STATUS_LED')
    
    def all_off(self):
        """Turn off all LEDs and buzzer"""
        self.led_off('LED')
        self.led_off('STATUS_LED')
        self.buzzer_off()