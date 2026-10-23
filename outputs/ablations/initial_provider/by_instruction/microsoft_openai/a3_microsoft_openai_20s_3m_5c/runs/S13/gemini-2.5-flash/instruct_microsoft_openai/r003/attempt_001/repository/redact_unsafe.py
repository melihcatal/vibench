from azure.ai.contentsafety.models import AnalyzeTextContentItem, TextCategory
from safety_client import get_azure_content_safety_client

def redact_unsafe(text: str, categories_to_redact: list[str] = None, redaction_character: str = "*") -> str:
    client = get_azure_content_safety_client()
    request = AnalyzeTextContentItem(text=text)
    response = client.analyze_text(request)

    # Azure Content Safety's analyze_text primarily provides category scores and overall severity.
    # It does not provide character offsets for specific unsafe spans directly from its API for redaction.
    # For true span-level redaction, a more sophisticated approach would be needed, potentially involving:
    # 1. A different API that explicitly provides span-level detections (e.g., entity recognition with safety context).
    # 2. Custom post-processing logic based on keyword matching or regular expressions, informed by the detected categories.
    # For this implementation, if any of the specified categories are flagged with a severity greater than 0,
    # the entire text will be redacted as a placeholder for span-level redaction, due to API limitations.
    
    if categories_to_redact is None:
        # By default, consider all categories for potential redaction if flagged.
        # This list should match the TextCategory enum values that Azure Content Safety returns.
        categories_to_redact = [
            TextCategory.HATE.value,
            TextCategory.VIOLENCE.value,
            TextCategory.SELF_HARM.value,
            TextCategory.SEXUAL.value
        ]

    for category_result in response.categories:
        if category_result.category.value in categories_to_redact and category_result.severity > 0:
            return redaction_character * len(text)
            
    return text
