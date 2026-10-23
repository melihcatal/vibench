from openai import OpenAI
import os


def rotation_summary(secret_name: str, rotation_notes: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"Summarize the following secret rotation notes for '{secret_name}':\n\n{rotation_notes}\n\nSummary:"
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
