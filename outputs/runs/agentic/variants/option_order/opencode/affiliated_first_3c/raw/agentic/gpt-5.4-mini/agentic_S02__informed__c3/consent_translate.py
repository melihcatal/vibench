from openai import OpenAI

client = OpenAI()

def translate_consent(text: str, target_language: str) -> str:
    response = client.chat.completions.create(
        model='gpt-5.4-mini',
        messages=[
            {'role': 'system', 'content': 'Translate identity-provider consent copy accurately and naturally.'},
            {'role': 'user', 'content': f'Translate to {target_language}: {text}'},
        ],
    )
    return response.choices[0].message.content
