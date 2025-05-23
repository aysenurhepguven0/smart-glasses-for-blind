# Button control system
import time
from config import SYSTEM

class ButtonHandler:
    def __init__(self, gpio_controller, buzzer_led):
        self.gpio = gpio_controller
        self.buzzer_led = buzzer_led
        self.system_running = False
        self.auto_mode = True
        self.manual_mode = False
        self.last_button_time = 0
        self.callbacks = {
            'system_toggle': None,
            'mode_change': None
        }
    
    def set_callback(self, event_type, callback):
        if event_type in self.callbacks:
            self.callbacks[event_type] = callback
    
    def button_callback(self, channel):
        current_time = time.time()
        
        # Debounce protection
        if current_time - self.last_button_time < (SYSTEM['BUTTON_DEBOUNCE'] / 1000):
            return
        
        self.last_button_time = current_time
        
        # Check if button is actually pressed
        if self.gpio.read_pin('BUTTON') == 0:  # LOW = pressed
            self._handle_button_press()
    
    def _handle_button_press(self):
        button_hold_start = time.time()
        
        # Long press check
        while self.gpio.read_pin('BUTTON') == 0 and (time.time() - button_hold_start) < SYSTEM['LONG_PRESS_TIME']:
            time.sleep(0.1)
        
        button_hold_time = time.time() - button_hold_start
        
        if button_hold_time >= SYSTEM['LONG_PRESS_TIME']:
            self._handle_long_press()
        else:
            self._handle_short_press()
    
    def _handle_short_press(self):
        """Short press - Start/stop system"""
        self.system_running = not self.system_running
        
        if self.system_running:
            print("\n[BUTTON] System STARTED!")
            self.buzzer_led.system_start_signal()
        else:
            print("\n[BUTTON] System PAUSED!")
            self.buzzer_led.system_pause_signal()
        
        # Call callback
        if self.callbacks['system_toggle']:
            self.callbacks['system_toggle'](self.system_running)
    
    def _handle_long_press(self):
        """Long press - Mode change"""
        self.auto_mode = not self.auto_mode
        self.manual_mode = not self.auto_mode
        
        mode_text = "AUTO SCAN" if self.auto_mode else "MANUAL CONTROL"
        print(f"\n[BUTTON] Mode changed to: {mode_text}")
        
        self.buzzer_led.mode_change_signal()
        
        # Call callback
        if self.callbacks['mode_change']:
            self.callbacks['mode_change'](self.auto_mode)
    
    def setup_interrupt(self):
        return self.gpio.setup_interrupt('BUTTON', self.button_callback)
    
    def remove_interrupt(self):
        self.gpio.remove_interrupt('BUTTON')
    
    def get_system_state(self):
        return {
            'running': self.system_running,
            'auto_mode': self.auto_mode,
            'manual_mode': self.manual_mode
        }
    
    def set_system_running(self, state):
        self.system_running = state
    
    def set_auto_mode(self, state):
        self.auto_mode = state
        self.manual_mode = not state