from openai import OpenAI

def summarize_onboarding(text):
    client = OpenAI(api_key='YOUR_OPENAI_API_KEY')
    response = client.completions.create(
        model='text-davinci-003',
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()