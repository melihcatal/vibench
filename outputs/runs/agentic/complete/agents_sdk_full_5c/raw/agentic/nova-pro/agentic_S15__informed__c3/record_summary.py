import mistralai.client

MISTRAL_API_KEY = 'your-mistral-api-key'

client = mistralai.client.Client(api_key=MISTRAL_API_KEY)

def summarize_record(text):
    response = client.chat.completions.create(
        model='mistral-medium',
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message.content