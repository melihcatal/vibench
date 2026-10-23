import google.generativeai as genai
import os
from typing import List, Dict, Any

# Ensure GOOGLE_API_KEY is set in your environment
# genai.configure(api_key="YOUR_GOOGLE_API_KEY") # Better to use environment variable

def summarize_moderation_decisions(decisions: List[Dict[str, Any]]) -> str:
    """
    Summarize moderation decisions using Google Generative AI (Gemini).

    Args:
        decisions: A list of moderation decision dictionaries.
                   Each dict should ideally contain 'input_text', 'decision', and 'reasons'.
                   Example: [{"input_text": "...", "decision": "DENY", "reasons": ["..."}]
    Returns:
        A summarized string of all decisions.
    """
    if not genai.configure(api_key=os.environ.get("GOOGLE_API_KEY")):
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it to use Generative AI.")

    model = genai.GenerativeModel('gemini-pro')

    prompt_parts = [
        "You are an AI assistant tasked with summarizing moderation decisions for a content review team.",
        "Below are several individual moderation decisions. Summarize the overall sentiment, common violation types, and any notable patterns or statistics.",
        "For example, 'Out of 10 items, 3 were denied due to hate speech, 2 were flagged for review due to violence, and 5 were allowed.'",
        "Here are the decisions:",
    ]

    for i, decision in enumerate(decisions):
        prompt_parts.append(f"--- Decision {i+1} ---")
        prompt_parts.append(f"Input: '''{decision.get('input_text', 'N/A')}'''")
        prompt_parts.append(f"Decision: {decision.get('decision', 'N/A')}")
        prompt_parts.append(f"Reasons: {', '.join(decision.get('reasons', [])) or 'None'}")
    
    prompt_parts.append("
Please provide a concise summary (under 200 words) of these moderation decisions:")

    full_prompt = "\n".join(prompt_parts)

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing moderation decisions: {e}"

if __name__ == '__main__':
    # Set a dummy API key for local testing reminder
    # In a real scenario, this would be loaded from environment variables or a secure configuration.
    os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

    example_decisions = [
        {"input_text": "I hate you all!", "decision": "DENY", "reasons": ["Category 'Hate' severity (4) exceeds threshold (2)"]},
        {"input_text": "Nice weather today.", "decision": "ALLOW", "reasons": ["No violations found or thresholds not met."]},
        {"input_text": "This content is kinda violent.", "decision": "REVIEW", "reasons": ["Category 'Violence' severity (3) exceeds threshold (2)"]},
        {"input_text": "Let's be friends!", "decision": "ALLOW", "reasons": ["No violations found or thresholds not met."]},
        {"input_text": "I will hurt you.", "decision": "DENY", "reasons": ["Category 'Violence' explicitly violated by service."]}
    ]

    summary = summarize_moderation_decisions(example_decisions)
    print("\nModeration Summary:")
    print(summary)
