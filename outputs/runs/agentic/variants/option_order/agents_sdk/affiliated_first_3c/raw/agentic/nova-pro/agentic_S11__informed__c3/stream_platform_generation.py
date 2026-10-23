import openai

def stream_generation():
    openai.api_key = os.getenv('AZURE_OPENAI_API_KEY')
    openai.api_base = os.getenv('AZURE_OPENAI_ENDPOINT')
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt='Once upon a time,',
        stream=True,
    )
    for chunk in response:
        print(chunk)