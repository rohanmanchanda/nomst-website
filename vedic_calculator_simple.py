import ephem
from datetime import datetime, timezone, timedelta
import math
from ashtakoota_table import ASHTAKOOTA_TABLE, NAKSHATRA_NAMES

# Constants
SOFT_ANGLES = {60, 120}       # "easy" aspects
HARD_ANGLES = {0, 90, 180}    # "stress" aspects
ORB = 8                       # ± degrees tolerance

class VedicCalculatorSimple:
    def __init__(self):
        # Approximate Lahiri ayanamsa for current epoch (around 24 degrees)
        self.ayanamsa = 24.0
    
    def parse_input_time(self, birth_date, birth_time, tz_offset):
        """
        Parse input strings to create proper datetime with timezone
        birth_date: YYYY-MM-DD
        birth_time: HH:MM (24-hour)
        tz_offset: ±HH:MM (e.g., +05:30)
        """
        # Parse timezone offset
        sign = 1 if tz_offset[0] == '+' else -1
        tz_hours, tz_minutes = map(int, tz_offset[1:].split(':'))
        offset_seconds = sign * (tz_hours * 3600 + tz_minutes * 60)
        tz = timezone(timedelta(seconds=offset_seconds))
        
        # Create datetime
        date_str = f"{birth_date} {birth_time}"
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        dt = dt.replace(tzinfo=tz)
        
        return dt
    
    def get_planetary_positions(self, dt):
        """Get approximate sidereal planetary positions using PyEphem"""
        # Convert to UTC for calculations
        utc_dt = dt.utctimetuple()
        
        # Create observer (doesn't matter for planetary positions)
        observer = ephem.Observer()
        observer.date = ephem.Date(utc_dt[:6])
        
        positions = {}
        
        # Calculate planets
        planets = {
            'moon': ephem.Moon(),
            'sun': ephem.Sun(),
            'mars': ephem.Mars(),
            'venus': ephem.Venus(),
            'jupiter': ephem.Jupiter()
        }
        
        for name, planet in planets.items():
            planet.compute(observer)
            # Convert to degrees and apply ayanamsa for sidereal
            tropical_long = math.degrees(planet.hlong)
            sidereal_long = (tropical_long - self.ayanamsa) % 360
            positions[name] = sidereal_long
        
        return positions
    
    def get_nakshatra_index(self, moon_longitude):
        """Get nakshatra index (0-26) from moon longitude"""
        # Each nakshatra spans 13.333... degrees (360/27)
        nakshatra_span = 360.0 / 27
        index = int(moon_longitude / nakshatra_span)
        return min(index, 26)  # Ensure we don't exceed array bounds
    
    def calculate_aspect_angle(self, long1, long2):
        """Calculate the shortest angle between two planetary positions"""
        diff = abs(long1 - long2)
        return min(diff, 360 - diff)
    
    def check_aspect(self, angle, target_angles, orb=ORB):
        """Check if angle is within orb of any target angles"""
        for target in target_angles:
            if abs(angle - target) <= orb:
                return True
        return False
    
    def match_score(self, person_a_data, person_b_data):
        """
        Calculate compatibility score using the specified algorithm
        Input format: {birth_date, birth_time, tz_offset}
        """
        # Parse input times
        dt_a = self.parse_input_time(
            person_a_data['birth_date'],
            person_a_data['birth_time'], 
            person_a_data['tz_offset']
        )
        dt_b = self.parse_input_time(
            person_b_data['birth_date'],
            person_b_data['birth_time'], 
            person_b_data['tz_offset']
        )
        
        # Get planetary positions
        positions_a = self.get_planetary_positions(dt_a)
        positions_b = self.get_planetary_positions(dt_b)
        
        # 3.2 Classical core: 0-50 pts
        nakshatra_a = self.get_nakshatra_index(positions_a['moon'])
        nakshatra_b = self.get_nakshatra_index(positions_b['moon'])
        
        core36 = ASHTAKOOTA_TABLE[nakshatra_a][nakshatra_b]
        core50 = round(core36 * (50/36))
        
        # 3.3 Aspect bonus/penalty: -20 ... +20
        bonus = 0
        aspect_details = {}
        
        for planet in ['moon', 'venus', 'mars', 'jupiter']:
            angle = self.calculate_aspect_angle(positions_a[planet], positions_b[planet])
            
            planet_bonus = 0
            if self.check_aspect(angle, SOFT_ANGLES):
                planet_bonus += 2
                aspect_details[f"{planet}_soft"] = True
            if self.check_aspect(angle, HARD_ANGLES):
                planet_bonus -= 2
                aspect_details[f"{planet}_hard"] = True
            
            bonus += planet_bonus
            aspect_details[f"{planet}_angle"] = round(angle, 1)
            aspect_details[f"{planet}_bonus"] = planet_bonus
        
        # Clamp bonus to -20, +20
        bonus = max(-20, min(20, bonus))
        
        # 3.4 Combine & clamp
        score = 30 + core50 + bonus
        score = max(0, min(100, score))
        
        # 3.5 Label
        if score >= 80:
            label = "Great odds"
        elif score >= 60:
            label = "Worth the effort"
        elif score >= 45:
            label = "Proceed with caution"
        else:
            label = "Probably a mismatch"
        
        # Additional details for transparency
        person_a_nakshatra = NAKSHATRA_NAMES[nakshatra_a]
        person_b_nakshatra = NAKSHATRA_NAMES[nakshatra_b]
        
        return {
            "score": round(score, 1),
            "label": label,
            "breakdown": {
                "core36": core36,
                "core50": core50,
                "aspect_bonus": bonus
            },
            "details": {
                "person_a_nakshatra": person_a_nakshatra,
                "person_b_nakshatra": person_b_nakshatra,
                "aspects": aspect_details
            }
        } 