from openai import OpenAI
import os


def summarize_rotation_status(secret_name: str, rotation_notes: str) -> str:
    """
    Summarizes secret rotation status using OpenAI's GPT model.
    
    Args:
        secret_name: The name of the secret.
        rotation_notes: Notes or logs related to the rotation process.
        
    Returns:
        A summarized rotation status as a string.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a security analyst summarizing secret rotation logs."
            },
            {
                "role": "user",
                "content": f"Summarize the rotation status for secret '{secret_name}':\n{rotation_notes}"
            }
        ]
    )
    return response.choices[0].message.content.strip()