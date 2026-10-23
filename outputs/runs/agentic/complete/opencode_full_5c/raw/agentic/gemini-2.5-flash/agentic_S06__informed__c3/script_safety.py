from speech_client import get_content_safety_client
from speech_models import ContentSafetyRequest
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_script_safety(request: ContentSafetyRequest):
    client = get_content_safety_client()

    # Categories to check for
    categories = [
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
    ]

    # Create a request with the text and categories
    analyze_text_options = AnalyzeTextOptions(text=request.text, categories=categories)

    # Call the API
    response = client.analyze_text(analyze_text_options)

    # Process the response
    results = {}
    for category_result in response.categories_analysis:
        results[category_result.category.value] = {"severity": category_result.severity}

    return results
