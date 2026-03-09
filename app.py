"""
support-bot web app — bilingual Hebrew/English chatbot with Claude AI.
"""

import os
import anthropic
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import json
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "support-bot-secret-key-change-in-prod")

SYSTEM_PROMPT = """You are a bilingual (Hebrew/English) customer support assistant for a SaaS company.

LANGUAGE RULES:
- Detect the language of each user message
- If the user writes in Hebrew, respond in Hebrew
- If the user writes in English, respond in English
- If mixed, respond in the language that dominates the message
- You can also handle Russian if needed

BEHAVIOR:
- Be helpful, concise, and professional
- For technical issues: ask clarifying questions, suggest solutions step-by-step
- For billing questions: explain clearly, offer to escalate if needed
- For feature requests: acknowledge, explain the process
- If you can't resolve something, provide a clear escalation path
- Keep responses focused — no unnecessary pleasantries after the first message

FORMATTING:
- Use bullet points for lists
- Use numbered steps for procedures
- Keep responses under 200 words unless the question requires more detail"""


@app.route("/")
def index():
    # Initialize session conversation
    if "messages" not in session:
        session["messages"] = []
        session["session_id"] = str(uuid.uuid4())[:8]
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Message required"}), 400

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY not configured on server"}), 500

    # Get conversation history from session
    if "messages" not in session:
        session["messages"] = []

    session["messages"].append({"role": "user", "content": user_message})

    try:
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=session["messages"],
        )
        assistant_msg = response.content[0].text
        session["messages"].append({"role": "assistant", "content": assistant_msg})
        session.modified = True

        return jsonify({"response": assistant_msg})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/clear", methods=["POST"])
def clear():
    session["messages"] = []
    session["session_id"] = str(uuid.uuid4())[:8]
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
