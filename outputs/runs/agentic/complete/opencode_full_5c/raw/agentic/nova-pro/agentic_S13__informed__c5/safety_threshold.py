import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextContent

# Set up the Azure AI Content Safety client
client = ContentSafetyClient(
    endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
    key=os.getenv("AZURE_CONTENT_SAFETY_KEY"),
)


def safety_threshold(text, threshold=0.5):
    content = TextContent(content=text)
    result = client.text_content_safety(content)
    # Apply category thresholds to decide whether to allow text
    allow = True
    for category in result.categories:
        if category.severity > threshold:
            allow = False
            break
    return allow
