from model_client import AzureModelClient

client = AzureModelClient()
response = client.invoke_model('text-davinci-003', 'Once upon a time,')
client.synthesize_speech(response.text, 'en-US', 'audio.wav')