import os
import openai

def summarize_rotation_status(status_text: str) -> str:
    """
    Summarizes the provided secret rotation status text using OpenAI's API.

    Args:
        status_text: A string containing details about a secret rotation event.

    Returns:
        A concise summary of the status.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes security events. Be concise.",
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following secret rotation status:\n\n{status_text}",
                },
            ],
            temperature=0.5,
            max_tokens=100,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        return f"An error occurred: {e}"

