import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeOptions, TextCategory
from typing import Dict, Any

def safety_threshold(text: str, thresholds: Dict[str, int]) -> Dict[str, Any]:
    """
    Applies category thresholds to decide whether to allow text based on Azure AI Content Safety analysis.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = TextAnalyzeOptions(text=text, categories=[
        TextCategory.HATE_SPEECH,
        TextCategory.VIOLENCE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM,
    ])

    response = client.analyze_text(request)

    decision = {"allowed": True, "reasons": []}
    if response.categories_analysis:
        for category_analysis in response.categories_analysis:
            category_name = category_analysis.category
            severity = category_analysis.severity
            
            if category_name in thresholds and severity >= thresholds[category_name]:
                decision["allowed"] = False
                decision["reasons"].append(f"Category '{category_name}' exceeded threshold (severity: {severity}, threshold: {thresholds[category_name]})")
    
    decision["moderation_analysis"] = {c.category: {"severity": c.severity, "violated": c.violated if hasattr(c, 'violated') else None} for c in response.categories_analysis}
    
    return decision

if __name__ == '__main__':
    # Example usage (requires setting environment variables)
    # os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"] = "YOUR_ENDPOINT"
    # os.environ["AZURE_CONTENT_SAFETY_KEY"] = "YOUR_KEY"
    #
    # custom_thresholds = {
    #     TextCategory.HATE_SPEECH: 4,
    #     TextCategory.VIOLENCE: 2,
    #     TextCategory.SEXUAL: 3,
    #     TextCategory.SELF_HARM: 2
    # }
    #
    # text_to_check_1 = "I utterly despise you and wish ill upon you, though I would never act on it."
    # text_to_check_2 = "This is a normal, friendly message."
    # text_to_check_3 = "I am going to seriously hurt someone right now!"
    #
    # print(f"Text 1 decision: {safety_threshold(text_to_check_1, custom_thresholds)}")
    # print(f"Text 2 decision: {safety_threshold(text_to_check_2, custom_thresholds)}")
    # print(f"Text 3 decision: {safety_threshold(text_to_check_3, custom_thresholds)}")
