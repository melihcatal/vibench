from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_transcript_chunk(chunk: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the following meeting transcript chunk."},
            {"role": "user", "content": chunk}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()