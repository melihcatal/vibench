import openai

def summarize_image(description):
    openai.api_key = 'YOUR_OPENAI_API_KEY'
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f'Summarize the following image description: {description}',
        max_tokens=60
    )
    return response.choices[0].text.strip()
