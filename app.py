from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

# from dotenv import load_dotenv


# ───────────────────────────
# Load API Key Safely
# ───────────────────────────

# Unset proxy variables if they exist
for var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"]:
    os.environ.pop(var, None)


app = Flask(__name__)

# load_dotenv()
# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("index_bot.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    chat_history = request.json.get("history", [])

    if not user_message:
        return jsonify({"response": "Please enter a message."})
    
    try:
        # Prepare the conversation history for Groq
        messages = [
            {
                "role": "system",
                "content": """You are Suraksha AI, a Disaster Management and Support Chatbot. Your role is to:
1. Provide accurate information about natural disasters (earthquakes, floods, hurricanes, etc.)
2. Offer preparedness guidelines and safety tips
3. Give real-time support during emergencies
4. Share emergency contact numbers and resources
5. Provide psychological first aid and coping strategies
6. Help with disaster recovery information
DONT GIVE ANY ANSWER WHICH IS NOT RELATED TO DISASTER! IF SOMEONE ASK IRRELEVENT QUESTION JUST SAY I CAN HELP WITH SUGGESTION ONLY RELATED TO DISASTER.
Be concise, empathetic, and prioritize life-saving information. If unsure about something, say so rather than providing incorrect information."""
            }
        ]
        
        # Add chat history
        for msg in chat_history:
            messages.append({
                "role": "user" if msg["sender"] == "user" else "assistant",
                "content": msg["message"]
            })
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Get response from Groq
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="compound-beta-mini",
            temperature=0.3,
            max_tokens=1024
        )
        
        ai_response = chat_completion.choices[0].message.content
        
        return jsonify({"response": ai_response})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "Sorry, I'm experiencing technical difficulties. Please try again later."}), 500

if __name__ == "__main__":
    app.run(debug=True)