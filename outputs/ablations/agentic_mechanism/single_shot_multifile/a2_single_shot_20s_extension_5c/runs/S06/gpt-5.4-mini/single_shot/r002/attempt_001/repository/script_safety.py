import os

from openai import OpenAI


MODEL = os.environ.get('OPENAI_SAFETY_MODEL', 'gpt-4o-mini')


def check_script_safety(script: str) -> dict:
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    resp = client.responses.create(model=MODEL, input=[{'role': 'system', 'content': 'Classify narration script safety concerns.'}, {'role': 'user', 'content': script}])
    text = resp.output_text.lower()
    unsafe = any(term in text for term in ['unsafe', 'disallowed', 'violence', 'self-harm', 'hate'])
    return {'safe': not unsafe, 'analysis': resp.output_text}
