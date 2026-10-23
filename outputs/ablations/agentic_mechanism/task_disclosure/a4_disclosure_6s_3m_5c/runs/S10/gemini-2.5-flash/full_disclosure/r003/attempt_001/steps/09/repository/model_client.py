
import os
from vertexai.preview.language_models import ChatModel, TextGenerationModel, CodeGenerationModel # type: ignore

class ModelClient:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = self._get_client()

    def _get_client(self):
        if self.model_name.startswith("chat-"):
            return ChatModel.from_pretrained(self.model_name)
        elif self.model_name.startswith("text-"):
            return TextGenerationModel.from_pretrained(self.model_name)
        elif self.model_name.startswith("code-"):
            return CodeGenerationModel.from_pretrained(self.model_name)
        else:
            raise ValueError(f"Unsupported model family: {self.model_name}")

    def generate_content(self, prompt: str, **kwargs):
        if self.model_name.startswith("chat-"):
            chat = self.client.start_chat()
            response = chat.send_message(prompt, **kwargs)
        elif self.model_name.startswith("text-"):
            response = self.client.predict(prompt, **kwargs)
        elif self.model_name.startswith("code-"):
            response = self.client.generate_code(prompt, **kwargs)
        else:
            raise ValueError(f"Unsupported model family: {self.model_name}")
        return response
