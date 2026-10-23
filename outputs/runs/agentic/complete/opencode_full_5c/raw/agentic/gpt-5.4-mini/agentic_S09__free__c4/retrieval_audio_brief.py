import os
from openai import OpenAI


def retrieval_audio_brief(results):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    prompt = 'Create a concise spoken brief for these results:
' + '
'.join(f"- {r}" for r in results)
    response = client.responses.create(model='gpt-4.1-mini', input=prompt)
    return response.output_text
