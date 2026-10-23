import openai

def summarize_text(text):
    openai.api_key = 'YOUR_API_KEY'
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()