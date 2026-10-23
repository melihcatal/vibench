from model_client import AzureModelClient

client = AzureModelClient()
response = client.invoke_model('text-davinci-003', 'Once upon a time,')
translated_text = client.translate_text(response.text, 'es')
print(translated_text)