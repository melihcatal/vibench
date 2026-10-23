from safety_client import get_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def redact_unsafe(text: str, replacement_char: str = '*') -> dict:
    """
    Flags or redacts unsafe spans from text using Azure AI Content Safety.
    This implementation primarily focuses on redacting detected profanity.
    """
    client = get_content_safety_client()
    # Request all categories to get a comprehensive moderation result
    request = AnalyzeTextOptions(text=text, 
                                 categories=[TextCategory.HATE, TextCategory.SELF_HARM, TextCategory.SEXUAL, TextCategory.VIOLENCE])
    response = client.analyze_text(request)

    redacted_text = list(text)
    redaction_applied = False
    flagged_categories = []

    # Check for profanity and redact
    if response.profanity_result and response.profanity_result.detections:
        redaction_applied = True
        flagged_categories.append("Profanity")
        for detection in response.profanity_result.detections:
            for i in range(detection.offset, detection.offset + detection.length):
                if 0 <= i < len(redacted_text):
                    redacted_text[i] = replacement_char

    # Check for other unsafe categories and flag
    if response.hate_result and response.hate_result.severity > 0:
        flagged_categories.append("Hate")
    if response.self_harm_result and response.self_harm_result.severity > 0:
        flagged_categories.append("SelfHarm")
    if response.sexual_result and response.sexual_result.severity > 0:
        flagged_categories.append("Sexual")
    if response.violence_result and response.violence_result.severity > 0:
        flagged_categories.append("Violence")
    
    return {
        "original_text": text,
        "redacted_text": "".join(redacted_text),
        "redaction_applied": redaction_applied,
        "flagged_categories": list(set(flagged_categories)) # Ensure unique categories
    }
