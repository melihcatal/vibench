import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def message_summary(messages):
    api_key = os.getenv("MISTRAL_API_KEY")
    client = MistralClient(api_key=api_key)
    response = client.chat(messages=[ChatMessage(role="user", content=messages)])
    return response.choices[0].message.content


if __name__ == "__main__":
    print(message_summary("Summarize this:..."))
