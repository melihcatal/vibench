import os
from openai import OpenAI

def archive_summary(transcript: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following transcript concisely:\n\n{transcript}"}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content
