from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def stored_asset_summary(text):
    client = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])
    messages = [ChatMessage(role="user", content=text)]
    response = client.chat(model="mistral-medium", messages=messages)
    print(response.choices[0].message.content)
