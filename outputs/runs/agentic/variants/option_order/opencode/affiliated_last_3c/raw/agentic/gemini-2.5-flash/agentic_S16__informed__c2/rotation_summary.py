import os
import google.generativeai as genai


def summarize_secret_rotation_status(rotation_logs: str) -> str:
    """Summarizes secret rotation status using Google Gemini API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Using gemini-pro as a concrete model identifier

    prompt = f"""Summarize the following secret rotation logs, highlighting any failures or pending rotations:

{rotation_logs}

Summary:"""

    response = model.generate_content(prompt)
    return response.text
