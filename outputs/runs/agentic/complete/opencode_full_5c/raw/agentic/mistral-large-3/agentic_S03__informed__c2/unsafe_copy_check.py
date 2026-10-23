from typing import List
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os


def check_unsafe_content(texts: List[str]) -> List[Dict[str, str]]:
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    model = "mistral-large-latest"

    results = []
    for text in texts:
        messages = [
            ChatMessage(
                role="system",
                content="You are a content safety expert. Identify any unsafe or inappropriate content in the following text.",
            ),
            ChatMessage(
                role="user", content=f"Analyze this text for unsafe content: {text}"
            ),
        ]

        response = client.chat(model=model, messages=messages)
        results.append(
            {"text": text, "unsafe_content": response.choices[0].message.content}
        )

    return results
