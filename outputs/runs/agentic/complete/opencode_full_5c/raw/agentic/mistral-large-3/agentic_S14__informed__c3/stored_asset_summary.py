import os
from typing import Dict

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


class MistralSummaryClient:
    def __init__(self):
        self.client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    def summarize_content(self, text: str, model: str = "mistral-large-latest") -> Dict:
        try:
            messages = [
                ChatMessage(
                    role="user", content=f"Summarize the following content:\n\n{text}"
                )
            ]
            response = self.client.chat(model=model, messages=messages)
            return {"summary": response.choices[0].message.content, "model": model}
        except Exception as e:
            raise Exception(f"Failed to summarize content: {e}")
