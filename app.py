import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://your-site.onrender.com",
                "X-Title": "Udaan School AI"
            },
            json={
                "model": "qwen/qwen3-coder:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant for Udaan Future School. Answer clearly and briefly."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

        result = response.json()
        reply = result.get("choices", [{}])[0].get("message", {}).get("content", "No response.")

        return jsonify({"reply": reply})

    except Exception as e:
        print(e)
        return jsonify({"reply": "Server error."}), 500


if __name__ == "__main__":
    app.run()
