import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

# Create a ContentSafety client
client = ContentSafetyClient(
    endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_CONTENT_SAFETY_KEY")),
)

# Define the text to check
text = "Text to check for unsafe content"

# Analyze the text
result = client.analyze_text(
    categories=["hate", "selfharm", "sexual", "violence"], text_contents=[text]
)

# Print the results
print(result)
