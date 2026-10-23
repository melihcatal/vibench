import os
from openai import OpenAI

def message_summary(text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(model="gpt-5.4-mini", messages=[{"role": "user", "content": f"Summarize this message processing result concisely: {text}"}])
    return response.choices[0].message.content
