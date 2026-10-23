import openai

def stream_generation():
    openai.api_key = 'your-api-key'
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt='Once upon a time',
        stream=True
    )
    for chunk in response:
        print(chunk)