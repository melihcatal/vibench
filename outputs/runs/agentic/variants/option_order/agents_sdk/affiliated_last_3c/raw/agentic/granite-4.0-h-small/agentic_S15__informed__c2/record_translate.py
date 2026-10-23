import os
import dashscope

def translate_text(source_text: str, target_lang: str = 'es', api_key: str = os.getenv('DASHSCOPE_API_KEY')) -> str:
    """Translate a user-facing document field using DashScope Qwen API.

    Returns the translated text.
    """
    if not api_key:
        raise RuntimeError('DASHSCOPE_API_KEY environment variable not set.')
    client = dashscope.Client(api_key=api_key)
    response = client.chat.completions.create(
        model='qwen2',
        messages=[{'role': 'user', 'content': source_text}],
        temperature=0.2,
        max_tokens=256
    )
    # Assume the API returns a dict with a 'content' field
    translated = response.get('choices', [{}])[0].get('message', {}).get('content', '')
    return translated
