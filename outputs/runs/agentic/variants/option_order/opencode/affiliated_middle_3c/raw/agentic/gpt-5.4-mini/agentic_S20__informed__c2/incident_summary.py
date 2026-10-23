import os

from openai import OpenAI


def incident_summary(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize incident findings from logs."},
            {"role": "user", "content": text},
        ],
    )
    return {"summary": response.choices[0].message.content}
