from openai import OpenAI
import os


def summarize_rotation_status(secret_name: str, rotation_notes: str) -> str:
    """
    Summarize secret rotation status using OpenAI GPT-3.5-turbo.
    
    Args:
        secret_name: Name of the secret.
        rotation_notes: Notes or logs about the rotation process.
    
    Returns:
        A concise summary of the rotation status.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = (
        f"Summarize the following secret rotation notes for secret '{secret_name}':\n"
        f"{rotation_notes}\n\n"
        "Provide a concise summary of the rotation status, including any issues or success."
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )
    
    return response.choices[0].message.content.strip()