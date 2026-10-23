import os
from typing import Dict, Any
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


class MistralSummarizer:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.model = "mistral-large-latest"
        self.client = MistralClient(api_key=self.api_key)

    def summarize_onboarding(self, onboarding_data: Dict[str, Any]) -> str:
        prompt = (
            f"Summarize the following onboarding data for support: {onboarding_data}"
        )
        messages = [ChatMessage(role="user", content=prompt)]
        response = self.client.chat(model=self.model, messages=messages)
        return response.choices[0].message.content


def onboarding_summary(onboarding_data: Dict[str, Any]) -> str:
    summarizer = MistralSummarizer()
    return summarizer.summarize_onboarding(onboarding_data)
