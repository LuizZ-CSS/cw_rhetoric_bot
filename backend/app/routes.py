from flask import Flask, request, session, jsonify
from app.chatbot import generate_response
from app.memory_handler import update_memory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "Rhetorica_memory_session"

@app.route("/")
def home():
    return "Rhetorica Bot is running! Try /ask?q=What is leadership"

@app.route("/favicon.ico")
def favicon():
    return "", 204  # Empty response with "No Content" status


@app.route("/ask", methods=["GET"])
def ask():
    """Handles user queries and returns a response."""
    question = request.args.get("q", "")
    alignment = int(request.args.get("alignment", "2"))
    scene = int(request.args.get("scene", "0"))

    if "memory" not in session:
        session["memory"] = []

    session["memory"], past = update_memory(session["memory"], f"User: {question}")
    answer = generate_response(question, alignment, scene)
    session["memory"].append(f"Rhetorica: {answer}")

    return jsonify({"response": answer})

@app.route("/train", methods=["POST"])
def train():
    """Allows adding new responses via API."""
    data = request.json
    keyword = data.get("keyword")
    context = data.get("context", "formal")
    answer = data.get("answer")

    if not keyword or not answer:
        return jsonify({"error": "Keyword and answer required"}), 400

    # Here, you can implement logic to save new responses dynamically.
    return jsonify({"message": f"Response for '{keyword}' trained successfully!"})
