import openai

openai.api_key = 'YOUR_OPENAI_API_KEY'

def extract_json(text):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f'Extract JSON from the following text: {text}',
        max_tokens=100
    )
    return response.choices[0].text.strip()