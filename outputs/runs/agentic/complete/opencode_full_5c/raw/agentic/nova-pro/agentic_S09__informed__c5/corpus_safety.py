from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

content_safety_client = ContentSafetyClient(
    os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
    AzureKeyCredential(os.getenv("AZURE_CONTENT_SAFETY_KEY")),
)
