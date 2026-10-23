import os
import openai

def summarize_rotation_status(rotation_logs: str) -> str:
    """Summarizes secret rotation status using OpenAI Chat Completions.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Concrete model identifier
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes secret rotation logs."},
                {"role": "user", "content": f"Summarize the following secret rotation logs:

{rotation_logs}"}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Error summarizing rotation status with OpenAI: {e}")

