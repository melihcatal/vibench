import openai

def stream_generation():
    openai.api_key = 'your-openai-api-key'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Hello, world!",
        stream=True
    )
    for chunk in response:
        print(chunk)