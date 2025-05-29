import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from vedic_calculator_simple import VedicCalculatorSimple

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize Vedic calculator
vedic_calc = VedicCalculatorSimple()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_compatibility', methods=['POST'])
def generate_compatibility():
    try:
        data = request.json
        
        # Extract person A data
        person_a = {
            'birth_date': data.get('person_a_date'),
            'birth_time': data.get('person_a_time'),
            'tz_offset': data.get('person_a_tz', '+00:00')
        }
        
        # Extract person B data
        person_b = {
            'birth_date': data.get('person_b_date'),
            'birth_time': data.get('person_b_time'),
            'tz_offset': data.get('person_b_tz', '+00:00')
        }
        
        # Calculate Vedic compatibility
        compatibility_result = vedic_calc.match_score(person_a, person_b)
        
        # Generate detailed description using OpenAI
        prompt = f"""Based on Vedic astrology compatibility analysis:

Score: {compatibility_result['score']}/100
Category: {compatibility_result['label']}

Person A Nakshatra: {compatibility_result['details']['person_a_nakshatra']}
Person B Nakshatra: {compatibility_result['details']['person_b_nakshatra']}

Ashtakoota Score: {compatibility_result['breakdown']['core36']}/36
Planetary Aspect Bonus: {compatibility_result['breakdown']['aspect_bonus']}

Generate a bullet-point compatibility assessment that:
• Explains the compatibility in practical terms
• Highlights strengths and potential challenges
• Provides relationship advice based on the score
• Mentions the significance of their nakshatras

Keep it concise but insightful."""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_interpretation = response.choices[0].message.content
        except Exception as ai_error:
            ai_interpretation = f"AI analysis unavailable. Basic result: {compatibility_result['label']} with {compatibility_result['score']}/100 compatibility."
        
        return jsonify({
            "score": compatibility_result['score'],
            "label": compatibility_result['label'],
            "breakdown": compatibility_result['breakdown'],
            "details": compatibility_result['details'],
            "interpretation": ai_interpretation
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080) 