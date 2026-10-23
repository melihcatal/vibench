from openai import OpenAI
import os

def summarize_rotation_status(rotation_status: str) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize secret rotation status reports concisely, highlighting key events, status, and actions needed."},
            {"role": "user", "content": rotation_status}
        ],
        max_tokens=200,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()