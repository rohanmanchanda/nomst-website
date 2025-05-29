#!/usr/bin/env python3

"""
Simple test script to verify the Vedic astrology app functionality
"""

import json
from vedic_calculator_simple import VedicCalculatorSimple

def test_vedic_calculator():
    print("🔮 Testing Vedic Astrology Calculator...")
    print("=" * 50)
    
    # Initialize calculator
    calc = VedicCalculatorSimple()
    
    # Test data
    person_a = {
        'birth_date': '1990-05-15',
        'birth_time': '14:30',
        'tz_offset': '+05:30'
    }
    
    person_b = {
        'birth_date': '1992-08-22',
        'birth_time': '09:15',
        'tz_offset': '+05:30'
    }
    
    try:
        # Calculate compatibility
        result = calc.match_score(person_a, person_b)
        
        print("✅ CALCULATION SUCCESSFUL!")
        print(f"Score: {result['score']}/100")
        print(f"Label: {result['label']}")
        print(f"Person A Nakshatra: {result['details']['person_a_nakshatra']}")
        print(f"Person B Nakshatra: {result['details']['person_b_nakshatra']}")
        print(f"Ashtakoota Score: {result['breakdown']['core36']}/36")
        print(f"Aspect Bonus: {result['breakdown']['aspect_bonus']}")
        
        print("\n🎯 DETAILED BREAKDOWN:")
        print(json.dumps(result, indent=2))
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_imports():
    print("\n📦 Testing Imports...")
    print("=" * 30)
    
    try:
        import ephem
        print("✅ PyEphem imported successfully")
        
        from ashtakoota_table import ASHTAKOOTA_TABLE, NAKSHATRA_NAMES
        print("✅ Ashtakoota table imported successfully")
        print(f"   - Table size: {len(ASHTAKOOTA_TABLE)} x {len(ASHTAKOOTA_TABLE[0])}")
        print(f"   - Nakshatra count: {len(NAKSHATRA_NAMES)}")
        
        from vedic_calculator_simple import VedicCalculatorSimple
        print("✅ Vedic calculator imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

def test_flask_app():
    print("\n🌐 Testing Flask App...")
    print("=" * 25)
    
    try:
        from app import app
        print("✅ Flask app imported successfully")
        
        # Test client
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page loads successfully")
            else:
                print(f"❌ Home page error: {response.status_code}")
                return False
                
            # Test API endpoint
            test_data = {
                'person_a_date': '1990-05-15',
                'person_a_time': '14:30',
                'person_a_tz': '+05:30',
                'person_b_date': '1992-08-22',
                'person_b_time': '09:15',
                'person_b_tz': '+05:30'
            }
            
            response = client.post('/generate_compatibility', 
                                 json=test_data,
                                 content_type='application/json')
            
            if response.status_code == 200:
                result = response.get_json()
                print(f"✅ API endpoint works! Score: {result.get('score', 'N/A')}")
            else:
                print(f"❌ API endpoint error: {response.status_code}")
                print(f"Response: {response.get_data(as_text=True)}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 VEDIC ASTROLOGY APP FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Run tests
    imports_ok = test_imports()
    calc_ok = test_vedic_calculator()
    flask_ok = test_flask_app()
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    print(f"Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Calculator: {'✅ PASS' if calc_ok else '❌ FAIL'}")
    print(f"Flask App: {'✅ PASS' if flask_ok else '❌ FAIL'}")
    
    if imports_ok and calc_ok and flask_ok:
        print("\n🎉 ALL TESTS PASSED! Your app is ready to deploy! 🎉")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.") 