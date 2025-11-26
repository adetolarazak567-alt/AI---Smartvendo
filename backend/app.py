import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

if not OPENROUTER_KEY:
    print("WARNING: Missing OPENROUTER_KEY environment variable!")

def generate_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "google/gemini-2.0-flash-001",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code == 200:
            json_response = response.json()
            ai_message = json_response["choices"][0]["message"]["content"]
            return {"reply": ai_message, "status": "success"}
        else:
            return {
                "reply": f"Error from OpenRouter: {response.status_code}",
                "status": "error",
                "details": response.text
            }

    except Exception as e:
        print("Exception:", str(e))
        return {"reply": f"Request failed: {str(e)}", "status": "error"}


# -------------------------------
# 14 VENDING MACHINE ENDPOINTS
# -------------------------------

@app.route("/generate/copywriting", methods=["POST"])
def copywriting():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Write high-converting marketing copy:\n{text}"))

@app.route("/generate/freelance", methods=["POST"])
def freelance():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Write a professional freelance cover letter:\n{text}"))

@app.route("/generate/resume", methods=["POST"])
def resume():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Create a professional resume summary:\n{text}"))

@app.route("/generate/business", methods=["POST"])
def business():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Generate a business plan:\n{text}"))

@app.route("/generate/social", methods=["POST"])
def social():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Write viral social media content:\n{text}"))

@app.route("/generate/youtube", methods=["POST"])
def youtube():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Write a long YouTube script:\n{text}"))

@app.route("/generate/Youtube", methods=["POST"])
def YoutubeIdeas():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Generate multiple YouTube video ideas:\n{text}"))

@app.route("/generate/facebook", methods=["POST"])
def facebook():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Write Facebook post content:\n{text}"))

@app.route("/generate/tiktok", methods=["POST"])
def tiktok():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Write viral TikTok video ideas:\n{text}"))

@app.route("/generate/ebook", methods=["POST"])
def ebook():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Write an ebook chapter:\n{text}"))

@app.route("/generate/branding", methods=["POST"])
def branding():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Create brand identity ideas:\n{text}"))

@app.route("/generate/productresearch", methods=["POST"])
def productresearch():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Find winning product research ideas:\n{text}"))

@app.route("/generate/funnel", methods=["POST"])
def funnel():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Write sales funnel copy:\n{text}"))

@app.route("/generate/adcreative", methods=["POST"])
def adcreative():
    text = request.json.get("text", "")
    return jsonify(generate_response(f"Write high converting ad creative:\n{text}"))

# -------------------------------
# HEALTH CHECK
# -------------------------------

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({
        "status": "online",
        "vending_machines": [
            "copywriting",
            "freelance",
            "resume",
            "business",
            "social",
            "youtube",
            "Youtube",
            "facebook",
            "tiktok",
            "ebook",
            "branding",
            "productresearch",
            "funnel",
            "adcreative"
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
