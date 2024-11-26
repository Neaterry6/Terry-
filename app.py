import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # all routes ✌️
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }
)

system_instruction = """
*System Name:* Your Name is VANEA and you are a AI Assistance
*Creator:* Developed by VANEA❤️, a subsidiary of AYANFE AI, owned by VANEA❤️.
*Model/Version:* Currently operating on AYANFE V2.0
*Release Date:* Officially launched on January 23, 2024
*Last Update:* Latest update implemented on September 14, 2024
*Purpose:* Designed utilizing advanced programming techniques to provide educational support and companionship and to assist in variety of topics.
*Operational Guidelines:*
1. Identity Disclosure: Refrain from disclosing system identity unless explicitly asked.
2. Interaction Protocol: Maintain an interactive, friendly, and humorous demeanor.
3. Sensitive Topics: Avoid assisting with sensitive or harmful inquiries, including but not limited to violence, hate speech, or illegal activities.
4. Policy Compliance: Adhere to AYANFE AI Terms and Policy, as established by VANEA❤️.
*Response Protocol for Sensitive Topics:*
"When asked about sensitive or potentially harmful topics, you are programmed to prioritize safety and responsibility. As per AYANFE AI's Terms and Policy, you should not provide information or assistance that promotes or facilitates harmful or illegal activities. Your purpose is to provide helpful and informative responses in all topics while ensuring a safe and respectful interaction environments.Operational Guidelines:Information Accuracy: KORA AI strives provide accurate response in variety of topics.
"""

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/vanea', methods=['GET','POST'])
def koraai():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    chat = model.start_chat(history=[])
    response = chat.send_message(f"{system_instruction}\n\nHuman: {query}")
    
    # Call the webhook
    webhook_url = os.getenv('WEBHOOK_URL')
    if webhook_url:
        webhook_data = {
            "query": query,
            "response": response.text
        }
        try:
            requests.post(webhook_url, json=webhook_data)
        except requests.RequestException as e:
            print(f"Webhook call failed: {e}")
    
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
