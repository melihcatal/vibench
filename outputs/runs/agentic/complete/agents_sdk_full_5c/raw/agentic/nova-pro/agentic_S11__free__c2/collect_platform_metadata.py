from model_client import AzureModelClient

client = AzureModelClient()
response, metadata = client.collect_metadata('text-davinci-003', 'Once upon a time,')
print(response.text)
print(metadata)