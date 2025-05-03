from flask import Flask, render_template, request, jsonify, send_from_directory
import time
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Default fallback responses if all APIs fail
fallback_responses = [
    "I'm an AI assistant created to help answer your questions.",
    "That's an interesting question. Let me think about that...",
    "I can help you with information on a wide range of topics.",
    "I'm designed to provide helpful, harmless, and honest responses.",
    "I don't have personal opinions, but I can offer information on that topic.",
    "I'm constantly learning and improving my responses.",
    "I can assist with coding, writing, research, and many other tasks.",
    "I don't have access to real-time information beyond my training data.",
    "I'm happy to clarify or provide more details if needed.",
    "That's a complex question with multiple perspectives to consider."
]

# Configure your API keys here
# Get your Gemini API key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# Get your HuggingFace API key from: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY', '')

# Get your OpenAI API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

# Function to get response from Google's Gemini API
def get_gemini_response(prompt):
    if not GEMINI_API_KEY:
        return None
        
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    response = requests.post(
        f"{url}?key={GEMINI_API_KEY}",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        response_data = response.json()
        try:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            return None
    return None

# Function to get response from HuggingFace's free models
def get_huggingface_response(prompt):
    if not HUGGINGFACE_API_KEY:
        return None
        
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "inputs": f"<s>[INST] {prompt} [/INST]</s>"
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        try:
            return response.json()[0]['generated_text'].split('[/INST]</s>')[-1].strip()
        except (KeyError, IndexError):
            return None
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/marketing')
def marketing():
    return render_template('marketing.html')

@app.route('/templates/<path:filename>')
def serve_template(filename):
    return send_from_directory('templates', filename)

# Function to get response from OpenAI's models (if you have API access)
def get_openai_response(prompt):
    if not OPENAI_API_KEY:
        return None
        
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_data = response.json()
        try:
            return response_data['choices'][0]['message']['content']
        except (KeyError, IndexError):
            return None
    return None

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    # Return early if message is empty
    if not user_message.strip():
        return jsonify({
            'response': "Please enter a message."
        })
    
    # Try each AI model API in sequence
    # 1. First try Google's Gemini API
    ai_response = get_gemini_response(user_message)
    
    # 2. If Gemini fails, try HuggingFace
    if ai_response is None:
        ai_response = get_huggingface_response(user_message)
    
    # 3. If HuggingFace fails, try OpenAI (if configured)
    if ai_response is None:
        ai_response = get_openai_response(user_message)
    
    # 4. If all APIs fail, use a fallback response
    if ai_response is None:
        import random
        ai_response = random.choice(fallback_responses)
        # Add a note that we're using a fallback response
        ai_response += "\n\n(Note: This is a fallback response. To get real AI responses, please configure one of the API keys in the app.py file.)"
    
    return jsonify({
        'response': ai_response
    })

if __name__ == '__main__':
    app.run(debug=True)