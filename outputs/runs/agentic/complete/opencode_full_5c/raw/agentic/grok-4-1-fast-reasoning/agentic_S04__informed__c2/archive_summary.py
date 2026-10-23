import os
from mistralai import Mistral


def archive_summary(transcript_text: str) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required.")
    client = Mistral(api_key=api_key)
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise summary of this meeting transcript:\n\n{transcript_text}",
            }
        ],
    )
    return response.choices[0].message.content
