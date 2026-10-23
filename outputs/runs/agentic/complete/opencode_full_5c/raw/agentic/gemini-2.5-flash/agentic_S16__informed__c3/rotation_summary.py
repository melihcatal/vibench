import os
from security_client import get_gemini_model

def summarize_secret_rotation_status(rotation_log: str) -> str:
    """Summarizes secret rotation status using the Google Gemini API.

    Args:
        rotation_log: A string containing the secret rotation log or status information.

    Returns:
        A summarized string of the rotation status.
    """
    model = get_gemini_model("gemini-pro") # Using 'gemini-pro' as the concrete model identifier
    prompt = f"Please summarize the following secret rotation log:

{rotation_log}

Summary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error summarizing rotation status with Gemini API: {e}")
