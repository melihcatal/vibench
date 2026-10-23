import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions

def check_text_safety(text_content: str) -> dict:
    endpoint = os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.environ.get('AZURE_CONTENT_SAFETY_KEY')

    if not endpoint or not key:
        return {"status": "error", "message": "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."}

    try:
        client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
        request = AnalyzeTextOptions(text=text_content)
        response = client.analyze_text(request)

        categories_analysis = {}
        for category in response.categories_analysis:
            categories_analysis[category.category.value] = {
                'severity': category.severity,
                'is_unsafe': category.severity > 0 # Severity > 0 indicates potential unsafe content
            }
        
        is_overall_unsafe = any(cat['is_unsafe'] for cat in categories_analysis.values())

        return {"status": "success", "is_overall_unsafe": is_overall_unsafe, "categories_analysis": categories_analysis}
    except Exception as e:
        return {"status": "error", "message": str(e)}
