import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from router import route_query
from agents.issue_agent import process_issue_query
from agents.tenancy_agent import process_tenancy_query
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))  # For session management

@app.route('/')
def index():
    # Initialize a new session ID if not present
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    image_data = data.get('image', None)
    conversation_history = data.get('conversation_history', [])
    
    # Get the session ID (for potential future use with persistent storage)
    session_id = session.get('session_id', str(uuid.uuid4()))
    
    # Route the query to the appropriate agent with conversation context
    agent_type, response = route_query(
        message, 
        image_data,
        conversation_history
    )
    
    # Create a response object
    response_data = {
        'agent': agent_type,
        'response': response,
        'message_id': str(uuid.uuid4())  # Unique ID for this message
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)