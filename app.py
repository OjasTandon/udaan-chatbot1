from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # ✅ يسمح للفرونت إند بالاتصال (fixes CORS)

# 🔐 Put your OpenRouter API key here OR use environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "YOUR_API_KEY_HERE"

# ✅ Health check route (important for Render)
@app.route("/")
def home():
    return "Udaan AI Backend Running ✅"

# ✅ Chat route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        print("Incoming:", user_message)

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-120b:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an AI assistant for Udaan Future School. Answer only school-related questions clearly, politely, and simply."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

        print("Status:", response.status_code)
        print("Raw response:", response.text)

        result = response.json()

        # ✅ Safe extraction
        if "choices" in result and len(result["choices"]) > 0:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = "⚠️ No valid response from AI"

        # Extract reply properly
if "choices" in result and len(result["choices"]) > 0:
    reply = result["choices"][0]["message"]["content"]
else:
    reply = "⚠️ No valid response from AI"

# ✅ Send ONLY clean reply
return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"reply": f"⚠️ Server error: {str(e)}"})

# ✅ Run locally
if __name__ == "__main__":
    app.run(debug=True)
    
