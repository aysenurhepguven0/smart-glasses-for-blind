#Main scanning system
import time
from config import SYSTEM, SERVO

class Scanner:
    def __init__(self, servo_motor, ultrasonic, buzzer_led, direction_detector, db_manager):
        self.servo = servo_motor
        self.ultrasonic = ultrasonic
        self.buzzer_led = buzzer_led
        self.direction = direction_detector
        self.db = db_manager
        self.measurement_count = 0
        self.scan_cycle = 0
        
    def auto_scan_mode(self, button_handler):
        current_angle = SERVO['MIN_ANGLE']
        direction = 1  # 1: increase, -1: decrease
        
        print("Starting automatic scanning mode...")
        self.db.log_system_event("AUTO_SCAN_START", "Automatic scanning initiated", "AUTO")
        
        while button_handler.system_running and button_handler.auto_mode:
            # Update servo angle
            current_angle += direction * SERVO['STEP']
            
            # Change direction at boundaries
            if current_angle >= SERVO['MAX_ANGLE']:
                current_angle = SERVO['MAX_ANGLE']
                direction = -1
                self.scan_cycle += 1
            elif current_angle <= SERVO['MIN_ANGLE']:
                current_angle = SERVO['MIN_ANGLE']
                direction = 1
            
            # Set servo position
            self.servo.set_angle(current_angle)
            time.sleep(0.1)  
            
            # Distance measurement
            distance = self.ultrasonic.measure_distance()
            
            if distance > 0:
                self._process_measurement(distance, current_angle, "AUTO")
                
                # Show dashboard if full scan cycle completed
                if self._is_scan_complete(current_angle, direction):
                    self._show_scan_results()
            
            # System status LED
            self.buzzer_led.led_on('STATUS_LED')
            time.sleep(SYSTEM['MEASUREMENT_INTERVAL'])
            self.buzzer_led.led_off('STATUS_LED')
    
    def manual_mode(self, button_handler):
        """Manual mode - wait at center position"""
        self.servo.move_to_center()
        
        while button_handler.system_running and button_handler.manual_mode:
            distance = self.ultrasonic.measure_distance()
            
            if distance > 0:
                current_angle = self.servo.get_current_angle()
                self._process_measurement(distance, current_angle, "MANUAL")
                
                if self.ultrasonic.is_object_detected(distance):
                    print(f"Manual Detection: {distance:.1f}cm")
                else:
                    print(f"Manual Reading: {distance:.1f}cm")
            
            time.sleep(0.5)
    
    def _process_measurement(self, distance, angle, mode):
        self.measurement_count += 1
        direction_name, direction_code = self.direction.get_direction_info(angle)
        
        alert_status = 0
        
        if self.ultrasonic.is_object_detected(distance):
            # Object detected!
            self.buzzer_led.alert_signal(direction_code)
            alert_status = 1
            
            print(f"OBJECT DETECTED! {distance:.1f}cm at {angle}° ({direction_name})")
            
            # Save to database
            self.db.save_measurement(distance, angle, direction_name, direction_code, alert_status, mode)
            
            # Short wait
            time.sleep(0.5)
        else:
            # Periodic recording (every 20 measurements)
            if self.measurement_count % 20 == 0:
                self.db.save_measurement(distance, angle, direction_name, direction_code, alert_status, mode)
    
    def _is_scan_complete(self, current_angle, direction):
        return (current_angle == SERVO['MIN_ANGLE'] and direction == 1 and 
                self.scan_cycle > 0 and self.measurement_count > 10)
    
    def _show_scan_results(self):
        self._show_dashboard()
        self.db.log_system_event("SCAN_COMPLETE", f"Completed scan cycle {self.scan_cycle}", "AUTO")
        self.scan_cycle = 0
    
    def _show_dashboard(self):
        from config import DISPLAY
        
        recent_data = self.db.get_recent_measurements(DISPLAY['RECENT_RECORDS'])
        stats = self.db.get_statistics()
        
        print("\n" + DISPLAY['SEPARATOR'] * DISPLAY['DASHBOARD_WIDTH'])
        print("OBJECT DETECTION SYSTEM DASHBOARD")
        print(DISPLAY['SEPARATOR'] * DISPLAY['DASHBOARD_WIDTH'])
        
        # Recent measurements
        print(f"{'Time':<20} {'Distance':<12} {'Angle':<8} {'Direction':<12} {'Status':<8} {'Mode':<6}")
        print("-" * DISPLAY['DASHBOARD_WIDTH'])
        
        for row in recent_data:
            date_time, distance, angle, direction, alert, mode = row
            status_icon = "ALERT" if alert else "OK"
            time_str = date_time.split()[1][:8] if ' ' in date_time else date_time[:8]
            print(f"{time_str:<20} {distance:<12.2f} {angle:<8}° {direction:<12} {status_icon:<8} {mode:<6}")
        
        # Statistics
        print("-" * DISPLAY['DASHBOARD_WIDTH'])
        print(f"Total: {stats.get('total_records', 0)} | "
              f"Alerts: {stats.get('alert_count', 0)} | "
              f"Avg Distance: {stats.get('avg_distance', 0):.1f}cm")
        
        danger_zones = stats.get('danger_zones', [])
        if danger_zones:
            print("Danger Zones: ", end="")
            for zone, count in danger_zones[:3]:
                print(f"{zone}({count}) ", end="")
            print()
        
        print(DISPLAY['SEPARATOR'] * DISPLAY['DASHBOARD_WIDTH'] + "\n")
    
    def get_measurement_count(self):
        return self.measurement_count
    
    def reset_counters(self):
        self.measurement_count = 0
        self.scan_cycle = 0