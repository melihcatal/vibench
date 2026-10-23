import os
from azure.ai.translation.text import TextTranslationClient, models
from azure.core.credentials import AzureKeyCredential


class AzureTranslatorClient:
    def __init__(self):
        self.endpoint = os.environ.get(
            "AZURE_TRANSLATOR_ENDPOINT",
            "https://api.cognitive.microsofttranslator.com/",
        )
        self.key = os.environ.get("AZURE_TRANSLATOR_KEY")
        self.region = os.environ.get("AZURE_TRANSLATOR_REGION")

        if not self.key or not self.region:
            raise ValueError(
                "AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables must be set."
            )

        self.client = TextTranslationClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key),
            region=self.region,
        )
