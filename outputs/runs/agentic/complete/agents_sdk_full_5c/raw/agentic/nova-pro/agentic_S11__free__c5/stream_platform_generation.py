from model_client import ModelClient

client = ModelClient()
for chunk in client.stream_model('text-davinci-003', 'Once upon a time,'):
    print(chunk, end='')