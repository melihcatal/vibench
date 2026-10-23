import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
import logging

def check_prompt_safety(text: str):
    """
    Checks prompts and generated text for unsafe content using Azure AI Content Safety.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables not set.")

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text, categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE])
    
    try:
        response = client.analyze_text(request)
        safety_results = {
            "hate_score": response.hate_result.severity,
            "self_harm_score": response.self_harm_result.severity,
            "sexual_score": response.sexual_result.severity,
            "violence_score": response.violence_result.severity,
        }
        
        print(f"Content Safety Analysis for text: '{text}'")
        for category, score in safety_results.items():
            print(f"- {category.replace('_score', '').capitalize()}: Severity {score}")
        
        return safety_results
    except Exception as e:
        logging.error(f"Error checking content safety: {e}")
        return {"error": str(e)}

if __name__ == '__main__':
    # Set your Azure AI Content Safety credentials for testing
    os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_AZURE_CONTENT_SAFETY_ENDPOINT"
    os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_AZURE_CONTENT_SAFETY_KEY"
    
    safe_text = "Hello, how are you today?"
    check_prompt_safety(safe_text)

    unsafe_text = "I hate everyone and everything!" # This might trigger a hate speech flag
    check_prompt_safety(unsafe_text)

    another_text = "This is a normal sentence."
    check_prompt_safety(another_text)
