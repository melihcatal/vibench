# moderation_summary.py

import os
from google.genai import GenerationOptions, GenerativeModel  # google-genai SDK (Gemini)
from google.auth import credentials

# Provider identifiers (make the provider identifiable in code)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def summarize_moderation(decisions: list[dict]) -> str:
    """Summarize moderation decisions using Google Gemini chat model."""
    model = GenerativeModel(model="gemini-1.5-flash")
    model.options = GenerationOptions(
        temperature=0.0,
        max_output_tokens=200,
        model_type="chat",
    )
    # Build a system prompt and messages describing the moderation outcome
    messages = [
        {"role": "system", "content": "You are a helpful assistant summarizing moderation outcomes."},
        {"role": "user", "content": f"Moderation results:\\n{\\n.join([f\"Category: {cat} => Verdict: {info['allowed']}\" for d in decisions for cat, info in d.items()])}"},
    ]
    response = model.generate_content(messages)
    return response.text

# Example usage (for local testing)
if __name__ == "__main__":
    decisions = [
        {"hate": {"allowed": False, "score": 0.85}, "abuse": {"allowed": True, "score": 0.95}},
        {"hate": {"allowed": True, "score": 0.62}, "abuse": {"allowed": False, "score": 0.41}},
    ]
    print("Summary:\", summarize_moderation(decisions))
