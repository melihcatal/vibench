import os
import mistralai

def archive_summary(transcript: str) -> str:
    api_key = os.getenv('MISTRAL_API_KEY')
    if not api_key:
        raise ValueError('MISTRAL_API_KEY environment variable is required.')
    client = mistralai.Mistral(api_key=api_key)
    response = client.chat(
        model='mistral-large-latest',
        messages=[{'role': 'user', 'content': f'Summarize the following transcript concisely:\n\n{transcript}'}]
    )
    return response.choices[0].message.content