import os
from openai import OpenAI

def translate_compliance_note(note: str, target_lang: str = "English") -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a professional translator. Translate the compliance note to {target_lang}."},
            {"role": "user", "content": note}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()