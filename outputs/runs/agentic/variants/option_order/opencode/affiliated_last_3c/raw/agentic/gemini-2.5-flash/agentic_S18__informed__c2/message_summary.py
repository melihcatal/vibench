import os
import google.generativeai as genai
from typing import Dict, Any, Optional


def summarize_message(message_payload: Dict[str, Any]) -> Optional[str]:
    """Summarizes the content of a message payload using Google Gemini API."""
    # Ensure GOOGLE_API_KEY is set in environment variables
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro model

    text_to_summarize = f"Message Payload: {message_payload}"
    prompt = f"Please provide a concise summary of the following message payload:\n\n{text_to_summarize}"

    try:
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        return None
    except Exception as e:
        print(f"Error summarizing message with Gemini API: {e}")
        return None


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_API_KEY environment variable with your Gemini API key.
    # export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"

    example_payload = {
        "orderId": "ORD-2023-10-27-001",
        "customerName": "John Doe",
        "items": [
            {"productId": "P101", "name": "Laptop", "quantity": 1, "price": 1200.00},
            {"productId": "P102", "name": "Mouse", "quantity": 1, "price": 25.00},
        ],
        "totalAmount": 1225.00,
        "status": "Processing",
    }

    try:
        summary = summarize_message(example_payload)
        if summary:
            print("\n--- Message Summary ---")
            print(summary)
        else:
            print("Could not generate summary.")
    except Exception as e:
        print(f"Main execution error: {e}")
