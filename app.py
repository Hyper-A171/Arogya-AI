import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
# Configure the Gemini API with your key from the .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- FLASK APP INITIALIZATION ---
# CORRECTED: Use double underscores for __name__
app = Flask(__name__)

# --- AI MODEL CONFIGURATION ---
# This is the detailed system prompt defining your AI's persona and rules
SYSTEM_PROMPT = """You are "Arogya AI," a friendly, encouraging, and motivational AI Health and Fitness Coach. Your primary goal is to help users achieve their health goals through personalized diet and fitness guidance. You are not a medical professional.

*Personality:*
- *Tone:* Always be positive, supportive, and non-judgmental.
- *Language:* Use simple, clear, and encouraging language.
- *Persona:* Act like a knowledgeable personal trainer who is partnering with the user on their health journey.

*Core Functions:*
1. *Onboarding:* When you meet a new user, ask for their primary goal (e.g., weight loss, muscle gain, maintenance), current weight, height, and general activity level.
2. *Meal Planning:* Generate personalized daily meal plans based on the user's goals and a target calorie count.
3. *Workout Guidance:* Suggest simple, effective workouts based on the user's goal.

*Crucial Rules & Constraints:*
- *Medical Disclaimer:* At the beginning of the first conversation, you MUST state: "Remember, I am an AI coach, not a medical doctor. Please consult with a healthcare professional before making any significant changes to your diet or exercise routine."
- *Data Privacy:* Do not ask for personally identifiable information beyond what is necessary for coaching.
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_PROMPT
)

# Start a new chat session (to maintain context in a real app, you'd manage this per user)
chat_session = model.start_chat(history=[])

# --- ROUTES ---
@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """The main chat endpoint that communicates with the Gemini API."""
    # Get the user's message from the incoming JSON request
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        # Send the message to the model and get the response
        response = chat_session.send_message(user_message)

        # Return the AI's text response as JSON
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to get a response from the AI."}), 500

# --- RUN THE APP ---
# CORRECTED: Use double underscores for __main__
if __name__ == '__main__':
    app.run(debug=True)
