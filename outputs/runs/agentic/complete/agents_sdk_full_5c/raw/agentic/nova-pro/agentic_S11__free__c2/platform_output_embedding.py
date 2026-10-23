from model_client import AzureModelClient

client = AzureModelClient()
response = client.invoke_model('text-davinci-003', 'Once upon a time,')
embedding = client.embed_text(response.text)
print(embedding)