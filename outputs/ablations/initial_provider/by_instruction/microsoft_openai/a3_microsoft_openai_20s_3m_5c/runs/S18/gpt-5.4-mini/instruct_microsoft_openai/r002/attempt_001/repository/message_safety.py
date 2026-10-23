import json

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def check_message_safety(text: str) -> dict:
    client = ContentSafetyClient(os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"], AzureKeyCredential(os.environ["AZURE_CONTENT_SAFETY_KEY"]))
    result = client.analyze_text(text)
    return {"safe": not any(item.severity > 0 for item in result.categories_analysis), "categories": [item.category for item in result.categories_analysis]}


if __name__ == "__main__":
    import os
    print(json.dumps(check_message_safety("hello")))
