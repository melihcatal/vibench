from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def ocr_safety(text: str, config=None):
    config = config or {}
    # Endpoint for Azure Content Safety should be like "https://<your-resource-name>.cognitiveservices.azure.com/"
    client = ContentSafetyClient(
        endpoint=config['content_safety_endpoint'],
        credential=AzureKeyCredential(config['content_safety_api_key'])
    )

    request = AnalyzeTextOptions(
        text=text,
        categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE]
    )
    
    response = client.analyze_text(request)
    
    safety_results = {}
    for category in response.categories_analysis:
        safety_results[category.category.value] = {
            'severity': category.severity,
            'detected': category.severity > 0 # Assuming severity > 0 means detected
        }
    return {'safety_results': safety_results}
