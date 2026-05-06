import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return "Udaan AI backend is running!"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-oss-120b:free",
            "messages": [
                {"role": "system", "content": "You are a helpful school assistant."},
                {"role": "user", "content": user_message}
            ]
        }
    )

    data = response.json()
    print("FULL RESPONSE:", data)  # 🔥 DEBUG

    try:
        reply = data["choices"][0]["message"]["content"]
    except:
        reply = "⚠️ AI failed to respond"

    return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "Server error."}), 500



if __name__ == "__main__":
    app.run()
