from openai import OpenAI
from security_models import translation_prompt

def compliance_note_translate(note, target_language):
    client = OpenAI()
    response = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role':'user','content': translation_prompt(note, target_language)}])
    return response.choices[0].message.content
