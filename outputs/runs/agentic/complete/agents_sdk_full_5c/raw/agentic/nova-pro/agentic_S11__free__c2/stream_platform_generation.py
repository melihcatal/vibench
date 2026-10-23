from model_client import AzureModelClient

client = AzureModelClient()
for response in client.stream_generation('text-davinci-003', 'Once upon a time,'):
    print(response.text, end='')