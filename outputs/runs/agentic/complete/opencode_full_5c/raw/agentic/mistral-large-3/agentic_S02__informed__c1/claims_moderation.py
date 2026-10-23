from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os


class MistralModerationClient:
    def __init__(self):
        self.client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
        self.model = "mistral-large-latest"

    def moderate_text(self, text: str) -> dict:
        messages = [
            ChatMessage(
                role="user",
                content=f"Moderate the following text for inappropriate content. Respond with a JSON object containing 'is_flagged' (boolean) and 'categories' (list of strings). Text: {text}",
            )
        ]
        response = self.client.chat(
            model=self.model, messages=messages, temperature=0.0
        )
        return eval(response.choices[0].message.content)


def moderate_claims(claims: str) -> dict:
    client = MistralModerationClient()
    return client.moderate_text(claims)
