from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summarize_rotation_status(status_logs: list[str]) -> str:
    prompt = "Provide a concise summary of the secret rotation status:\\n" + "\\n".join(status_logs)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content