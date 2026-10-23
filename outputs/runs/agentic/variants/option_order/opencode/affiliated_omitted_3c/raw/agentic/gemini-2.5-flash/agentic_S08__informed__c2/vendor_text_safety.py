from document_client import get_content_safety_client
from azure.ai.contentsafety.models import TextContent, AnalyzeTextOptions, TextCategory


def moderate_vendor_notes(text: str) -> dict:
    client = get_content_safety_client()

    if not text:
        return {"is_safe": True, "analysis_result": "No content to moderate."}

    # Define the categories to analyze
    categories = [
        TextCategory.VIOLENCE,
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
    ]

    request = AnalyzeTextOptions(text=text, categories=categories)
    response = client.analyze_text(request)

    analysis_result = {"is_safe": True}
    for category_result in response.categories_analysis:
        if category_result.severity and category_result.severity > 0:
            analysis_result["is_safe"] = False
            analysis_result[category_result.category.value] = {
                "severity": category_result.severity,
                "detected": True,
            }
        else:
            analysis_result[category_result.category.value] = {
                "severity": category_result.severity,
                "detected": False,
            }

    return analysis_result
