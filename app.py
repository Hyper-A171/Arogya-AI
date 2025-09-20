import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from dotenv import load_dotenv
import google.generativeai as genai

# --- Firebase Admin SDK Setup ---
import firebase_admin
from firebase_admin import credentials, auth, firestore

load_dotenv()

# Initialize Firebase Admin
try:
    # The path comes from your .env file
    cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase App initialized successfully.")
except Exception as e:
    print(f"Error initializing Firebase App: {e}")
    # This is a critical error, the app cannot run without Firebase Admin
    exit()

# --- Flask App Initialization ---
app = Flask(__name__)
# This is where the FLASK_SECRET_KEY from your .env file is used
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# --- User Model & Flask-Login Setup ---
class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    """Loads a user from Firestore for the session."""
    try:
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return User(id=user_id, name=user_data.get('name'), email=user_data.get('email'))
    except Exception as e:
        print(f"Error loading user from Firestore: {e}")
    return None

# --- AI MODEL CONFIGURATION ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
SYSTEM_PROMPT = """You are "Arogya AI," a friendly, encouraging, and motivational AI Health and Fitness Coach...""" # Add your full prompt
model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

# --- Public & Auth Routes ---
@app.route('/')
def landing():
    """Serves the public landing page."""
    return render_template('landing.html')

@app.route('/signup')
def signup():
    """Serves the public signup page."""
    return render_template('signup.html')

@app.route('/login')
def login():
    """Serves the login page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard')) 
    return render_template('login.html')

@app.route('/session_login', methods=['POST'])
def session_login():
    """Receives ID token from client, verifies it, and creates a server session."""
    id_token = request.json.get('idToken')
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            user_data = {
                'name': decoded_token.get('name'),
                'email': decoded_token.get('email'),
                'created_at': firestore.SERVER_TIMESTAMP
            }
            user_ref.set(user_data)
        
        user = User(id=uid, name=decoded_token.get('name'), email=decoded_token.get('email'))
        login_user(user)
        
        return jsonify({"status": "success", "message": "User logged in."})
        
    except Exception as e:
        print(f"Error in session_login: {e}")
        return jsonify({"status": "error", "message": "Authentication failed."}), 401

@app.route('/logout')
@login_required
def logout():
    """Logs the user out."""
    logout_user()
    return redirect(url_for('landing'))

# --- Protected Application Routes ---
@app.route('/dashboard') 
@login_required
def dashboard(): 
    """Serves the main AI chat application."""
    return render_template('app.html', user=current_user)

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    """Handles chat with the AI."""
    user_message = request.json.get("message")
    # In a real app, manage chat history per user
    chat_session = model.start_chat(history=[]) 
    response = chat_session.send_message(user_message)
    return jsonify({"reply": response.text})

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)

import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from dotenv import load_dotenv
import google.generativeai as genai

# --- Firebase Admin SDK Setup ---
import firebase_admin
from firebase_admin import credentials, auth, firestore

load_dotenv()

# Initialize Firebase Admin
try:
    # The path comes from your .env file
    cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase App initialized successfully.")
except Exception as e:
    print(f"Error initializing Firebase App: {e}")
    # This is a critical error, the app cannot run without Firebase Admin
    exit()

# --- Flask App Initialization ---
app = Flask(__name__)
# This is where the FLASK_SECRET_KEY from your .env file is used
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# --- User Model & Flask-Login Setup ---
class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    """Loads a user from Firestore for the session."""
    try:
        user_doc = db.collection('users').document(user_id).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return User(id=user_id, name=user_data.get('name'), email=user_data.get('email'))
    except Exception as e:
        print(f"Error loading user from Firestore: {e}")
    return None

# --- AI MODEL CONFIGURATION ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
SYSTEM_PROMPT = """You are "Arogya AI," a friendly, encouraging, and motivational AI Health and Fitness Coach...""" # Add your full prompt
model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)

# --- Public & Auth Routes ---
@app.route('/')
def landing():
    """Serves the public landing page."""
    return render_template('landing.html')

@app.route('/signup')
def signup():
    """Serves the public signup page."""
    return render_template('signup.html')

@app.route('/login')
def login():
    """Serves the login page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard')) 
    return render_template('login.html')

@app.route('/session_login', methods=['POST'])
def session_login():
    """Receives ID token from client, verifies it, and creates a server session."""
    id_token = request.json.get('idToken')
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            user_data = {
                'name': decoded_token.get('name'),
                'email': decoded_token.get('email'),
                'created_at': firestore.SERVER_TIMESTAMP
            }
            user_ref.set(user_data)
        
        user = User(id=uid, name=decoded_token.get('name'), email=decoded_token.get('email'))
        login_user(user)
        
        return jsonify({"status": "success", "message": "User logged in."})
        
    except Exception as e:
        print(f"Error in session_login: {e}")
        return jsonify({"status": "error", "message": "Authentication failed."}), 401

@app.route('/logout')
@login_required
def logout():
    """Logs the user out."""
    logout_user()
    return redirect(url_for('landing'))

# --- Protected Application Routes ---
@app.route('/dashboard') 
@login_required
def dashboard(): 
    """Serves the main AI chat application."""
    return render_template('app.html', user=current_user)

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"reply": "⚠️ No message received."}), 400

        chat_session = model.start_chat(history=[]) 
        response = chat_session.send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"[ERROR in /chat] {e}")
        return jsonify({"reply": f"❌ Error: {str(e)}"}), 500

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)

