from messaging_client import get_gemini_model
import google.generativeai as genai


def summarize_message_payload(payload_text: str) -> str:
    """Summarizes a given message payload text using Google Gemini Pro."""
    model = get_gemini_model("gemini-pro")

    prompt = f"""Summarize the following message payload in one concise sentence:

{payload_text}
"""
    response = model.generate_content(prompt)
    return response.text.strip()
