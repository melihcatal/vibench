import mistralai.client

client = mistralai.client.Client(api_key='YOUR_MISTRAL_API_KEY')

def stream_completion(prompt):
    response = client.chat.completions.create(
        model='mistral-medium',
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='')
    print()