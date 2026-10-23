import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextContent

# Set up the Azure AI Content Safety client
client = ContentSafetyClient(
    endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
    key=os.getenv("AZURE_CONTENT_SAFETY_KEY"),
)


def redact_unsafe(text):
    content = TextContent(content=text)
    result = client.text_content_safety(content)
    # Redact unsafe spans based on the result
    redacted_text = text
    for category in result.categories:
        if category.severity > 0:
            redacted_text = redacted_text.replace(
                category.text, "*" * len(category.text)
            )
    return redacted_text
