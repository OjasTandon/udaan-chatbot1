from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # ✅ يسمح للفرونت إند بالاتصال (fixes CORS)

# 🔐 Put your OpenRouter API key here OR use environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "YOUR_API_KEY_HERE"

# ✅ Health check route (important for Render)
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

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
                        "content": "You are an AI assistant for Udaan Future School. Answer clearly and politely."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

        result = response.json()
        print("RAW:", result)  # debug

        # ✅ Extract message
        if "choices" in result and len(result["choices"]) > 0:
            reply = result["choices"][0]["message"]["content"]
        else:
            reply = "⚠️ AI did not return a valid answer"

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})

# ✅ Run locally
if __name__ == "__main__":
    app.run(debug=True)
    
