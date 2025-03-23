import sys
import requests
import re

BASE_URL = "http://localhost:5000/ask"

def ask_Rhetorica(question, context="formal"):
    """Send a query to the Rhetorica API and return the response."""
    response = requests.get(BASE_URL, params={"q": question, "context": context})
    
    if response.status_code == 200:
        data = response.json()
        if "response" in data and data["response"]:
            return data["response"]
        else:
            return "I am pondering upon that. Ask me something else?"
    return f"Error: {response.status_code} - {response.text}"

def extract_context_and_question(user_input):
    """Extracts context from the user input if provided inline (e.g., 'casual: What is leadership?')."""
    match = re.match(r'^(formal|casual|philosophical|academic|neutral|entertaining|sarcastic|mourning):\s*(.*)', user_input, re.IGNORECASE)
    if match:
        return match.group(2).strip(), match.group(1).lower()
    return user_input, "formal"  # Default to formal if no context is specified

def chat_loop():
    """Start the CLI chatbot loop with context support."""
    print("\n🤖 Welcome to Rhetorica Bot CLI! Type 'exit' or 'quit' to leave.\n")
    
    while True:
        user_input = input("> ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("\n👋 Goodbye! Talk to you next time!\n")
            sys.exit()
        
        question, context = extract_context_and_question(user_input)
        response = ask_Rhetorica(question, context)
        print(f"\n🗨️ Rhetorica ({context}): {response}\n")

if __name__ == "__main__":
    chat_loop()
