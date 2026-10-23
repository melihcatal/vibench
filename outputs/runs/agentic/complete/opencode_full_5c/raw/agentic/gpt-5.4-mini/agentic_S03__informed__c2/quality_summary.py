from openai import OpenAI


def quality_summary(text: str, source_language: str, target_language: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role': 'system', 'content': 'Summarize translation quality issues.'}, {'role': 'user', 'content': f'Source language: {source_language}
Target language: {target_language}
Text: {text}'}])
    return response.choices[0].message.content
