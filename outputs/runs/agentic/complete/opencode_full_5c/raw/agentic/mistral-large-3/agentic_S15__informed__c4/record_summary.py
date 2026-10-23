from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from typing import Dict, Any, List
from database_models import FetchResponse


class RecordSummarizer:
    def __init__(self):
        self.client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
        self.model = "mistral-large-latest"

    def summarize(self, document: Dict[str, Any]) -> str:
        prompt = f"Summarize the following document in 2-3 sentences:\n\n{document}"
        messages = [ChatMessage(role="user", content=prompt)]
        response = self.client.chat(model=self.model, messages=messages)
        return response.choices[0].message.content
