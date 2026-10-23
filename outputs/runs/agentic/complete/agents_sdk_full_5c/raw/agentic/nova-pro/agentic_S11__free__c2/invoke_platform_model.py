from model_client import AzureModelClient

client = AzureModelClient()
response = client.invoke_model('text-davinci-003', 'Once upon a time,')
print(response.text)