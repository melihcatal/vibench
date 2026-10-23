import os
from openai import OpenAI


def retrieval_audio_brief(results):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    text = ' '.join(result.get('title', '') + ' ' + result.get('snippet', '') for result in results).strip()
    completion = client.chat.completions.create(model='gpt-4o-mini', messages=[{'role': 'user', 'content': f'Create a short spoken brief from these search results: {text}'}])
    brief = completion.choices[0].message.content
    return {'provider': 'openai', 'model': 'gpt-4o-mini', 'brief': brief}
