import os
from openai import OpenAI
from security_models import RotationStatus

def summarize_rotation_status(status_report: str) -> str:
    """
    Uses OpenAI to summarize a secret rotation status report.

    Args:
        status_report: A text report describing rotation events.

    Returns:
        A concise summary of the report.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # OpenAI-specific model identifier
            messages=[
                {"role": "system", "content": "You are a security analyst assistant. Summarize the following secret rotation report concisely."},
                {"role": "user", "content": status_report}
            ],
            temperature=0.3,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        raise
