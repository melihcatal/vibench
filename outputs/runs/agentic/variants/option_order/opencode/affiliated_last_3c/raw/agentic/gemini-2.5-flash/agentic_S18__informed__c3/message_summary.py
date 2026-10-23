import os
import google.generativeai as genai
from messaging_models import MessageSummary
from typing import Dict, Any


def summarize_message_payload(
    message_id: str, payload: Dict[str, Any]
) -> MessageSummary:
    """
    Summarizes a message payload using the Google Gemini API.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    payload_str = str(payload)
    prompt = f"Summarize the following message payload in one concise sentence and extract 3-5 keywords: {payload_str}"

    response = model.generate_content(prompt)
    summary_text = response.text.strip()

    # Simple attempt to extract keywords, can be improved with more sophisticated NLP
    keywords = [
        word.strip().lower()
        for word in summary_text.split()
        if len(word) > 3 and word.isalpha()
    ]
    keywords = list(set(keywords[:5]))  # Get unique keywords, max 5

    return MessageSummary(
        message_id=message_id, summary_text=summary_text, keywords=keywords
    )


if __name__ == "__main__":
    # Example usage:
    # export GOOGLE_API_KEY="your-gemini-api-key"
    sample_payload = {
        "action": "order_placed",
        "order_id": "ORD789",
        "customer_id": "cust123",
        "items": [
            {"product_id": "prodA", "quantity": 2},
            {"product_id": "prodB", "quantity": 1},
        ],
        "total_amount": 150.75,
        "currency": "USD",
    }
    summary = summarize_message_payload("msg-1", sample_payload)
    print(f"Message Summary: {summary}")
