import os
import google.generativeai as genai
from security_models import SecretRotationStatus

def summarize_rotation_status(status: SecretRotationStatus) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set for Gemini API.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the rotation status for secret ID '{status.secret_id}'.
Last rotation date: {status.last_rotation_date if status.last_rotation_date else 'N/A'}
Next rotation date: {status.next_rotation_date if status.next_rotation_date else 'N/A'}
Rotation enabled: {status.rotation_enabled}
Provide a concise summary in one paragraph.'''

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error summarizing rotation status with Gemini API: {e}")
