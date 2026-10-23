from model_client import AzureModelClient

client = AzureModelClient()
response = client.invoke_model('text-davinci-003', 'Once upon a time,')
if response.sentiment.score > 0.5:
    print('Safe content')
else:
    print('Unsafe content')