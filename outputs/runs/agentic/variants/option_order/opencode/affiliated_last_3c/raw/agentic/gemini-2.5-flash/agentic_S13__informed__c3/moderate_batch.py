import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_batch(texts: list[str]):
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    batch_results = []
    for text in texts:
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)

        results = {
            category.category.value: category.severity
            for category in response.categories_analysis
        }
        batch_results.append(results)
    return batch_results
