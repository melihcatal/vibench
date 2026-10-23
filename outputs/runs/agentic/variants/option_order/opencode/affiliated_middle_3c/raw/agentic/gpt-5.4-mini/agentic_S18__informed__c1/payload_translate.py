import os
from openai import OpenAI

def payload_translate(text, target_language):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(model="gpt-5.4-mini", messages=[{"role": "user", "content": f"Translate the following customer-facing message into {target_language}: {text}"}])
    return response.choices[0].message.content
