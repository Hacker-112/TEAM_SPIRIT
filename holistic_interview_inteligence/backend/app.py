import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify, request
from flask_cors import CORS

import interview_state as state
import ollama_interview_engine as ai

app = Flask(__name__)
CORS(app)

# -------------------------------
# HOME
# -------------------------------
@app.route("/")
def home():
    return jsonify({"status": "Backend running"})


# -------------------------------
# START INTERVIEW
# -------------------------------
@app.route("/start_interview", methods=["POST"])
def start_interview():
    data = request.json
    role = data.get("role")

    if not role:
        return jsonify({"error": "Role is required"}), 400

    state.interview_running = True
    state.current_role = role
    state.current_question = ai.generate_question(role)

    return jsonify({
        "status": "Interview started",
        "question": state.current_question
    })


# -------------------------------
# GET CURRENT QUESTION
# -------------------------------
@app.route("/get_question", methods=["GET"])
def get_question():
    if not state.interview_running:
        return jsonify({"error": "Interview not running"}), 400

    return jsonify({
        "question": state.current_question
    })


# -------------------------------
# STOP INTERVIEW
# -------------------------------
@app.route("/stop_interview", methods=["POST"])
def stop_interview():
    state.interview_running = False
    state.current_role = None
    state.current_question = None

    return jsonify({"status": "Interview stopped"})


if __name__ == "__main__":
    app.run(debug=True)
