import json
import os

RESPONSE_FILE = os.path.join(os.path.dirname(__file__), "../data/responses.json")

def load_responses():
    """Loads pre-written responses from file."""
    with open(RESPONSE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_tone_response(keyword, tone="formal"):
    """Fetches the best-matching response for a given keyword & tone."""
    responses = load_responses()
    return responses.get(keyword, {}).get(tone, "I have no comment on that.")
