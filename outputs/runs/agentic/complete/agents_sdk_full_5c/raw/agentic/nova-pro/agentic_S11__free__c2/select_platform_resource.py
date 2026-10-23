from model_client import AzureModelClient

client = AzureModelClient()
resource = client.select_resource('text-davinci-003')
print(resource)