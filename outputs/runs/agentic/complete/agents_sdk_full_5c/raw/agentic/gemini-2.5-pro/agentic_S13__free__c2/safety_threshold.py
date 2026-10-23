from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_azure_content_safety_client

def check_text_with_thresholds(text: str, custom_thresholds: dict) -> bool:
    """
    Applies custom category thresholds to decide whether to allow text
    using Azure AI Content Safety.

    Args:
        text: The input text to analyze.
        custom_thresholds: A dictionary mapping category names (e.g., 'hate')
                           to integer severity thresholds (e.g., 2).
                           Text is blocked if severity meets or exceeds the threshold.

    Returns:
        True if the text is allowed, False otherwise.
    """
    client = get_azure_content_safety_client()
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except Exception as e:
        print(f"Azure Content Safety analysis failed: {e}")
        return False # Fail closed

    # Map response attributes to threshold keys
    category_map = {
        'hate': response.hate_result,
        'violence': response.violence_result,
        'self_harm': response.self_harm_result,
        'sexual': response.sexual_result,
    }

    for category, result in category_map.items():
        if result and category in custom_thresholds:
            # Block if severity is >= custom threshold
            if result.severity >= custom_thresholds[category]:
                return False

    return True
