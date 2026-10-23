import os
from azure.ai.contentsafety import ContentSafetyClient, ContentSafetyClientOptions
from azure.core.credentials import AzureKeyCredential

# Azure Content Safety credentials
credential = AzureKeyCredential(os.environ["AZURE_CONTENT_SAFETY_KEY"])

# Create a client
client = ContentSafetyClient(os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"], credential)

# Define the text to check
text = "This is a sample text to check for unsafe content"

# Check the text for unsafe content
response = client.classify_text(text)

# Print the results
print(response)
