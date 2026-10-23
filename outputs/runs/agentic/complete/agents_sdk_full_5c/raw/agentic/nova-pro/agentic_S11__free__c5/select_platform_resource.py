from model_client import ModelClient

client = ModelClient()
resource = client.select_model('text-davinci-003')
print(resource)