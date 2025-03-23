import requests
import json
import time

BASE_URL = "http://localhost:5000"  # Update if API is hosted elsewhere
OUTPUT_FILE = "test_results.txt"

# Define test cases (Question + Expected Behavior)
TEST_CASES = [
    # ✅ Normal questions (should return structured answers)
    ("What is diplomacy?", "formal"),  
    ("casual: What is leadership?", "casual"),  
    ("What is power?", "philosophical"),  
    ("Tell me about corruption.", "formal"),  
    ("sarcastic: What is revolution?", "sarcastic"),  
    ("What is persistence?", "neutral"),  

    # ✅ Memory recall tests
    ("Summarize what we've discussed.", "formal"),  # Should recall past responses
    ("What did we talk about?", "formal"),  # Should return a valid summary

    # ✅ Vague question handling (should avoid generic "It depends" responses)
    ("Tell me about the world.", "formal"),  # Shouldn't be vague
    ("Explain history.", "formal"),  # Should request clarification
    ("What is the meaning of life?", "philosophical"),  # Should return a deep answer

    # ✅ Follow-up hallucination blocking (should NOT generate "User: That makes sense..." lines)
    ("How does power relate to leadership?", "formal"),  
    ("What happens after a revolution?", "philosophical"),  

    # ✅ AI/Business hallucination prevention
    ("Tell me about predictive analytics.", "formal"),  # Should respond with "I'm not sure how that relates..."
    ("What is natural language processing?", "formal"),  # Should avoid AI/business discussion

    # ✅ Random input handling (should return "I'm not sure what that means.")
    ("What is zxqwe123?", "formal"),  
    ("Tiananmen1989", "formal"),  
    ("9/11", "formal"),  
    ("random123abc", "formal"),  
]

def run_test_case(question, context):
    """Sends a request to Rhetorica and logs the response."""
    response = requests.get(f"{BASE_URL}/ask", params={"q": question, "context": context})

    if response.status_code == 200:
        response_text = response.json().get("response", "No response received.")
    else:
        response_text = f"Error: {response.status_code} - {response.text}"

    return response_text

def run_tests():
    """Runs all test cases and saves output to a file."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"🚀 **Rhetorica Bot Test Results** 🚀\nTimestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for i, (question, context) in enumerate(TEST_CASES):
            print(f"\n🛠️ Running Test {i+1}: {question} ({context})\n")
            response = run_test_case(question, context)
            print(f"✅ Response: {response}\n")

            f.write(f"Test {i+1}: {question} ({context})\n")
            f.write(f"Response: {response}\n\n")

    print("\n🎉 All test cases completed! Check 'test_results.txt' for details.")

if __name__ == "__main__":
    run_tests()
