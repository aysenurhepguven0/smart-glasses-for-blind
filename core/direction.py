# Direction detection system
from config import DIRECTION

class DirectionDetector:
    def __init__(self):
        self.zones = DIRECTION['ZONES']
        self.beep_patterns = DIRECTION['BEEP_PATTERNS']
        
    def get_direction_info(self, angle):
        for zone_name, zone_info in self.zones.items():
            if zone_info['min'] <= angle <= zone_info['max']:
                return zone_info['name'], zone_info['code']
                
        # Return FRONT as default
        return 'FRONT', 3
        
    def get_beep_pattern(self, direction_code):
        return self.beep_patterns.get(direction_code, [(0.15, 0.05)])
        
    def is_danger_zone(self, direction_name):
        # FAR_LEFT and FAR_RIGHT can be considered more dangerous
        return direction_name in ['FAR_LEFT', 'FAR_RIGHT']
        
    def get_all_zones(self):
        return self.zones
        
    def angle_to_description(self, angle):
        direction_name, _ = self.get_direction_info(angle)
                
        descriptions = {
            'FAR_LEFT': 'Far left side',
            'LEFT': 'Left side',
            'FRONT': 'Front',
            'RIGHT': 'Right side',
            'FAR_RIGHT': 'Far right side'
        }
                
        return descriptions.get(direction_name, 'Unknown direction')
        
    def get_zone_coverage(self, angle_list):
        zone_coverage = {}
                
        for angle in angle_list:
            direction_name, _ = self.get_direction_info(angle)
            zone_coverage[direction_name] = zone_coverage.get(direction_name, 0) + 1
                
        return zone_coverage