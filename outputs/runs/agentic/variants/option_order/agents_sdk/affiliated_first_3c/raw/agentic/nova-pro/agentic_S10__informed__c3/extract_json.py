import openai

def extract_json(text):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f'Extract JSON from the following text: {text}',
        max_tokens=150
    )
    return response.choices[0].text.strip()