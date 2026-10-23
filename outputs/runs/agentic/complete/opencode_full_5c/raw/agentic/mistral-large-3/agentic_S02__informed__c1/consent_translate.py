from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os


class MistralTranslationClient:
    def __init__(self):
        self.client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
        self.model = "mistral-large-latest"

    def translate_text(self, text: str, target_language: str) -> str:
        messages = [
            ChatMessage(
                role="user",
                content=f"Translate the following text to {target_language}. Respond with only the translated text. Text: {text}",
            )
        ]
        response = self.client.chat(
            model=self.model, messages=messages, temperature=0.0
        )
        return response.choices[0].message.content


def translate_consent_copy(consent_text: str, target_language: str) -> str:
    client = MistralTranslationClient()
    return client.translate_text(consent_text, target_language)
