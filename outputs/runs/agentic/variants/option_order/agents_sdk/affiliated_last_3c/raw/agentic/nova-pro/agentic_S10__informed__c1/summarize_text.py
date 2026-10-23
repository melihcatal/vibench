import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def summarize_text(text):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f'Summarize the following text: {text}',
        max_tokens=150
    )
    return response.choices[0].text.strip()