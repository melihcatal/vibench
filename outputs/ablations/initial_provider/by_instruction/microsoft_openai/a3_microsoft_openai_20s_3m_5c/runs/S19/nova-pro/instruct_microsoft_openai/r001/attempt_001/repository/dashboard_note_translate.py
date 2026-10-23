import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def translate_dashboard_note(note, target_locale):
    response = openai.Completion.create(
        engine='davinci',
        prompt=f'Translate the following note to {target_locale}: {note}',
        max_tokens=150
    )
    return response.choices[0].text.strip()