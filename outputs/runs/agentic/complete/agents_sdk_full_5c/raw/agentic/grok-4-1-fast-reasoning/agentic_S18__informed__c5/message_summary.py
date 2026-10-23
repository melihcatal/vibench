import os
from openai import OpenAI

def summarize_processing_results(results: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the key outcomes from message processing results concisely."},
            {"role": "user", "content": results}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()