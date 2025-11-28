# app.py
import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

if not OPENROUTER_KEY:
    app.logger.warning("OPENROUTER_KEY not set. Set it in environment before production.")

def call_ai(prompt, model="gpt-3.5-turbo", max_tokens=900):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a concise, professional assistant that produces content optimized for the user's request."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }
    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data.get("choices", [{}])[0].get("message", {}).get("content") or data.get("result") or ""

# -------------------------
# EXISTING ENDPOINTS
# -------------------------
@app.route("/generate/copywriting", methods=["POST"])
def generate_copywriting():
    body = request.json or {}
    product = body.get("product") or body.get("topic")
    tone = body.get("tone", "persuasive and professional")
    length = body.get("length", "short")
    if not product:
        return jsonify({"error":"No product/topic provided"}), 400
    prompt = (
        f"Create {length} marketing copy for: {product}\n"
        f"Tone: {tone}\n\n"
        "Include:\n- 3 headline options\n- 2 short ad captions (max 120 chars)\n- 1 longer product description (3-4 sentences)\n- Suggested CTA (one line)"
    )
    try:
        out = call_ai(prompt)
        return jsonify({"copy": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate/freelance", methods=["POST"])
def generate_freelance():
    body = request.json or {}
    platform = body.get("platform", "Upwork/Fiverr")
    gig = body.get("gig") or body.get("service")
    brief = body.get("brief", "")
    if not gig:
        return jsonify({"error":"No gig/service provided"}), 400
    prompt = (
        f"Write an optimized freelance proposal for {platform} for this service: {gig}\n"
        f"Include a 1-sentence hook, a 3-paragraph proposal (short), and 3 bullet points of portfolio/examples. "
        f"User brief: {brief}"
    )
    try:
        out = call_ai(prompt)
        return jsonify({"proposal": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate/resume", methods=["POST"])
def generate_resume():
    body = request.json or {}
    info = body.get("info")
    role = body.get("target_role", "")
    if not info:
        return jsonify({"error":"No user info provided"}), 400
    prompt = (
        f"Using the following user info, produce a professional resume summary (3-5 bullet achievements), "
        f"a tailored work-experience bullet list for a target role: {role} (if provided), and a short LinkedIn headline + summary.\n\n"
        f"User info:\n{info}\n\nFormat clearly with headings: SUMMARY, EXPERIENCE HIGHLIGHTS, LINKEDIN HEADLINE, LINKEDIN SUMMARY."
    )
    try:
        out = call_ai(prompt)
        return jsonify({"resume": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate/business", methods=["POST"])
def generate_business():
    body = request.json or {}
    niche = body.get("niche") or body.get("topic")
    if not niche:
        return jsonify({"error":"No niche/topic provided"}), 400
    prompt = (
        f"Generate 10 business or side-hustle ideas for the niche: {niche}. "
        "For each idea give: a one-line description, target customer, three monetization channels, and a 3-step launch plan."
    )
    try:
        out = call_ai(prompt, max_tokens=1200)
        return jsonify({"ideas": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate/social", methods=["POST"])
def generate_social():
    body = request.json or {}
    platform = body.get("platform", "instagram")
    topic = body.get("topic")
    tone = body.get("tone", "engaging")
    if not topic:
        return jsonify({"error":"No topic provided"}), 400
    prompt = (
        f"For {platform}, create: 5 post caption ideas (short), 10 relevant hashtags, 3 short story prompts, "
        f"and a weekly posting schedule (3 posts/week) for the topic: {topic}. Tone: {tone}."
    )
    try:
        out = call_ai(prompt)
        return jsonify({"social": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------
# NEW HIGH-VALUE ENDPOINTS
# -------------------------

@app.route("/generate/productresearch", methods=["POST"])
def generate_product_research():
    body = request.json or {}
    niche = body.get("topic")
    if not niche:
        return jsonify({"error": "No niche/topic provided"}), 400
    prompt = (
        f"Perform AI product research for the niche: {niche}.\n"
        "Provide 10 product ideas with:\n- One-line description\n- Target customer\n- Selling points\n- Suggested marketing channels"
    )
    try:
        out = call_ai(prompt, max_tokens=1200)
        return jsonify({"ideas": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate/branding", methods=["POST"])
def generate_branding():
    body = request.json or {}
    text = body.get("text")
    if not text:
        return jsonify({"error": "No branding prompt provided"}), 400
    prompt = f"Generate premium branding and logo concepts:\n{text}"
    try:
        out = call_ai(prompt, max_tokens=900)
        return jsonify({"reply": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate/ebook", methods=["POST"])
def generate_ebook():
    body = request.json or {}
    text = body.get("text")
    if not text:
        return jsonify({"error": "No ebook prompt provided"}), 400
    prompt = f"Create an e-book based on the following request:\n{text}"
    try:
        out = call_ai(prompt, max_tokens=2000)
        return jsonify({"reply": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate/tiktok", methods=["POST"])
def generate_tiktok():
    body = request.json or {}
    topic = body.get("topic")
    if not topic:
        return jsonify({"error": "No topic provided"}), 400
    prompt = (
        f"Create 5 TikTok viral script ideas for the topic: {topic}.\n"
        "Include hooks, short dialogues, trends, and CTA lines."
    )
    try:
        out = call_ai(prompt, max_tokens=900)
        return jsonify({"social": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate/facebook", methods=["POST"])
def generate_facebook():
    body = request.json or {}
    topic = body.get("topic")
    if not topic:
        return jsonify({"error": "No topic provided"}), 400
    prompt = (
        f"Create 5 Facebook marketing content ideas for the niche: {topic}.\n"
        "Include short post captions, ad copy, CTA lines, and post hooks."
    )
    try:
        out = call_ai(prompt, max_tokens=900)
        return jsonify({"social": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# lowercase youtube for Growth Kit
@app.route("/generate/youtube", methods=["POST"])
def generate_youtube_lowercase():
    body = request.json or {}
    topic = body.get("topic")
    style = body.get("style", "storytelling")
    duration = body.get("duration", "5 minutes")
    if not topic:
        return jsonify({"error": "No topic provided"}), 400
    prompt = (
        f"Create a full YouTube script for this topic: {topic}\n"
        f"Video length: {duration}\n"
        f"Script style: {style}\n\n"
        "Include:\n- Hook (2–3 lines)\n- Intro\n- Sections with timestamps\n- Narration style lines\n- Natural YouTuber language\n- CTA at the end"
    )
    try:
        out = call_ai(prompt, max_tokens=1400)
        return jsonify({"script": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Sales funnel generator
@app.route("/generate/funnel", methods=["POST"])
def generate_funnel():
    body = request.json or {}
    product = body.get("product")
    audience = body.get("audience", "general customers")
    if not product:
        return jsonify({"error":"No product provided"}), 400
    prompt = (
        f"Generate a full sales funnel for this product: {product}\n"
        f"Target audience: {audience}\n\n"
        "Include:\n- Awareness copy\n- Lead magnet idea\n- Email sequence (3 emails)\n- Landing page copy\n- Objection breakers\n- Final CTA"
    )
    try:
        out = call_ai(prompt, max_tokens=1500)
        return jsonify({"funnel": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ad creative generator
@app.route("/generate/adcreative", methods=["POST"])
def generate_adcreative():
    body = request.json or {}
    product = body.get("product")
    platform = body.get("platform", "facebook ads")
    if not product:
        return jsonify({"error":"No product provided"}), 400
    prompt = (
        f"Create ad creatives for {platform}.\n"
        f"Product: {product}\n\n"
        "Include:\n- 3 headline options\n- 3 primary text variations (ad captions)\n- 3 CTA lines\n- 3 attention-grabbing hooks\n- A short script for video ads (15–30 secs)"
    )
    try:
        out = call_ai(prompt)
        return jsonify({"ads": out})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({
        "status": "ok",
        "services": [
            "copywriting","freelance","resume","business","social",
            "youtube","youtube_lowercase","facebook","tiktok","ebook",
            "branding","product_research","funnel","adcreative","Youtube_script"
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
