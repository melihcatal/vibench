import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def moderate_batch(texts: list[str]):
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    all_results = []
    for text in texts:
        request = AnalyzeTextOptions(text=text, categories=[
            TextCategory.VIOLENCE,
            TextCategory.HATE_SPEECH,
            TextCategory.SEXUAL,
            TextCategory.SELF_HARM
        ], output_type="FourPoint")
        response = client.analyze_text(request)

        results = {"text": text}
        for category in response.categories_analysis:
            results[category.category.value] = {
                "severity": category.severity
            }
        all_results.append(results)
    return all_results
