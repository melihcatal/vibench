import openai
import os

class TranslationClient:
    def __init__(self):
        self.client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2023-05-15",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.model_name = os.getenv("AZURE_OPENAI_MODEL_NAME", "gpt-4")

    def get_client(self):
        return self.client
    
    def get_model_name(self):
        return self.model_name
