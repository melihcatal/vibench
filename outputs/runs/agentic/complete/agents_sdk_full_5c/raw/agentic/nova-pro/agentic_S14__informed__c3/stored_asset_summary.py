from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

def stored_asset_summary(text):
    client = MistralClient(api_key='your-mistral-api-key')
    messages = [ChatMessage(role='user', content=text)]
    response = client.chat(model='mistral-tiny', messages=messages)
    return response.choices[0].message.content