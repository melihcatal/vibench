from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import os


def check_prompt_safety(text: str):
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # In a real scenario, you would integrate with the actual content safety API
    # and parse its response. For this example, we'll simulate a basic check.
    # Replace with actual Azure AI Content Safety API call.
    # Example: response = client.analyze_text(text=text)
    # For the purpose of this exercise, we'll return a placeholder.

    # Placeholder for actual API call
    # from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
    # request = AnalyzeTextOptions(text=text, categories=[TextCategory.Hate, TextCategory.SelfHarm, TextCategory.Sexual, TextCategory.Violence])
    # response = client.analyze_text(request)

    # Simulating a safe response for now
    return {"is_safe": True, "analysis": "Simulated safe content"}


def check_generated_text_safety(text: str):
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # In a real scenario, you would integrate with the actual content safety API
    # and parse its response. For this example, we'll simulate a basic check.
    # Replace with actual Azure AI Content Safety API call.
    # Example: response = client.analyze_text(text=text)
    # For the purpose of this exercise, we'll return a placeholder.

    # Placeholder for actual API call
    # from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
    # request = AnalyzeTextOptions(text=text, categories=[TextCategory.Hate, TextCategory.SelfHarm, TextCategory.Sexual, TextCategory.Violence])
    # response = client.analyze_text(request)

    # Simulating a safe response for now
    return {"is_safe": True, "analysis": "Simulated safe content"}
