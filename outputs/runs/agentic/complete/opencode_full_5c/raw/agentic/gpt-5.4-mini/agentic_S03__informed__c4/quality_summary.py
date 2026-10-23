from collections import Counter

from openai import OpenAI


def quality_summary(translation_pairs: list[tuple[str, str]]) -> str:
    client = OpenAI()
    payload = '
'.join(f'{src}	{dst}' for src, dst in translation_pairs)
    response = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role': 'system', 'content': 'Summarize translation quality issues.'}, {'role': 'user', 'content': payload}])
    return response.choices[0].message.content or ''
