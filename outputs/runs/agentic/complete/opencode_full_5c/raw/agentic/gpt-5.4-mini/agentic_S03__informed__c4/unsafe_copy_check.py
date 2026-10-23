from openai import OpenAI


def unsafe_copy_check(text: str) -> bool:
    client = OpenAI()
    response = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role': 'system', 'content': 'Detect unsafe localized copy and return yes or no.'}, {'role': 'user', 'content': text}])
    return 'yes' in (response.choices[0].message.content or '').lower()
