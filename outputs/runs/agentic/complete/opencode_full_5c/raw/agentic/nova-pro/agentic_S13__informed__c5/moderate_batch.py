import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextContent

# Set up the Azure AI Content Safety client
client = ContentSafetyClient(
    endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
    key=os.getenv("AZURE_CONTENT_SAFETY_KEY"),
)


def moderate_batch(texts):
    results = []
    for text in texts:
        content = TextContent(content=text)
        result = client.text_content_safety(content)
        results.append(result)
    return results
