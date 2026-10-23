from model_client import ModelClient

client = ModelClient()
response = client.invoke_model('text-davinci-003', 'Once upon a time,')
print(response.text, response.metadata)