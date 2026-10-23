import os
import google.generativeai as genai
from security_client import get_gemini_model

def summarize_secret_rotation_status(rotation_logs: str) -> str:
    """
    Summarizes secret rotation status using the Google Gemini API.
    Provider: Google Gemini API
    Model: gemini-pro
    """
    model = get_gemini_model()
    prompt = f"Summarize the following secret rotation logs:

{rotation_logs}

Summary:"
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY to be set)
    # sample_logs = """
    # Secret 'db-password' rotation initiated at 2023-01-01 10:00:00.
    # New version '5' created successfully.
    # Application 'backend-service' updated to use new version.
    # Old version '4' marked for destruction in 7 days.
    # Secret 'api-key-service' rotation failed at 2023-01-01 11:30:00: Permissions denied.
    # """
    # summary = summarize_secret_rotation_status(sample_logs)
    # print(f"Rotation Summary: {summary}")
    pass
