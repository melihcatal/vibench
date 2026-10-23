import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions

os.environ["AZURE_CONTENT_SAFETY_KEY"] = "your-api-key"
client = ContentSafetyClient(
    os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"], os.environ["AZURE_CONTENT_SAFETY_KEY"]
)
