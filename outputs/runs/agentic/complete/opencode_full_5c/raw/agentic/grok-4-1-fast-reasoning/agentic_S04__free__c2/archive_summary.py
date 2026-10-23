import os
from openai import OpenAI


def archive_summary(transcript_text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise summary of this meeting transcript:\\n\\n{transcript_text}",
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content
