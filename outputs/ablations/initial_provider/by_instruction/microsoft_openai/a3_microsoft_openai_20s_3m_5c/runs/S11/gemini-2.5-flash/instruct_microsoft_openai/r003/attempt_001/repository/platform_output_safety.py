from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import os

def check_output_safety(text: str):
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    
    if not endpoint or not key:
        return {"is_safe": True, "details": "Azure Content Safety credentials not set."}

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # In a real scenario, you'd integrate the text analysis request here.
    # For demonstration, we'll assume a basic check.
    # response = client.analyze_text(text=text)
    # For this example, we will just return a placeholder for safety check.
    return {"is_safe": True, "details": "Simulated content safety check with Azure AI Content Safety."}
