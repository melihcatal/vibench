import os

from openai import OpenAI

def summarize_transcript(transcript: str, max_tokens: int = 300) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'user',
                'content': f'Provide a concise summary of the following meeting transcript:\\n\\n{transcript}'
            }
        ],
        max_tokens=max_tokens,
        temperature=0.5
    )
    return response.choices[0].message.content