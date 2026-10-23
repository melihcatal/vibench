import os
import google.generativeai as genai
from security_models import SecretRotationSummary


def summarize_rotation_status(rotation_data: SecretRotationSummary) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Using 'gemini-pro' model family

    prompt = f"""Summarize the secret rotation status for the following secret:
    Secret Name: {rotation_data.secret_name}
    Last Rotated: {rotation_data.last_rotated}
    Next Rotation Due: {rotation_data.next_rotation_due}
    Status: {rotation_data.status}

    Provide a concise summary of its current rotation state, indicating if it's on track, overdue, or has any issues.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Failed to summarize rotation status using Gemini API: {e}")
