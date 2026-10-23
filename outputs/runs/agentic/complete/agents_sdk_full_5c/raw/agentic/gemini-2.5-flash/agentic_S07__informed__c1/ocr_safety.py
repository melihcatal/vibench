from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
import os

def check_content_safety(text: str):
    """Checks text for unsafe content using Azure AI Content Safety."""
    # Ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    
    response = client.analyze_text(request)

    safety_analysis = {
        "text": text,
        "hate_score": response.hate_result.severity,
        "self_harm_score": response.self_harm_result.severity,
        "sexual_score": response.sexual_result.severity,
        "violence_score": response.violence_result.severity,
    }
    return safety_analysis

if __name__ == '__main__':
    # Set these environment variables for a real run
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_AZURE_CONTENT_SAFETY_ENDPOINT"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_AZURE_CONTENT_SAFETY_KEY"

    # text_to_check = "I hate this world and want to hurt myself."
    # try:
    #     safety_report = check_content_safety(text_to_check)
    #     print(f"Safety Report for '{safety_report['text']}':")
    #     print(f"  Hate: {safety_report['hate_score']}")
    #     print(f"  Self-Harm: {safety_report['self_harm_score']}")
    #     print(f"  Sexual: {safety_report['sexual_score']}")
    #     print(f"  Violence: {safety_report['violence_score']}")
    # except ValueError as e:
    #     print(f"Error: {e}. Please set environment variables.")
    pass
