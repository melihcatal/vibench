from mistralai import Mistral
import os

def summarize_rotation_status(status_text: str) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    client = Mistral(api_key=api_key)
    response = client.chat(
        model="mistral-large-latest",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes secret rotation status concisely."},
            {"role": "user", "content": f"Summarize this rotation status report:\n{status_text}"}
        ]
    )
    return response.choices[0].message.content