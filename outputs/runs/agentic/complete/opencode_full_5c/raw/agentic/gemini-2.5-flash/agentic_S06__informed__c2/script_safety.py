import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from speech_client import get_azure_content_safety_client
from speech_models import ContentSafetyRequest


def check_script_safety(request: ContentSafetyRequest) -> dict:
    """Checks narration scripts for unsafe content using Azure AI Content Safety.

    Returns a dictionary with moderation analysis results.
    """
    client = get_azure_content_safety_client()

    text_categories = [
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
    ]

    request_body = AnalyzeTextOptions(
        text=request.text_content,
        categories=text_categories,
        blocklist_names=[],  # Add blocklist names if needed
        break_by_blocklists=False,
    )

    try:
        response = client.analyze_text(request_body)
        result = {"harm_analysis": [], "blocklist_matches": []}

        if response.hate_result:
            result["harm_analysis"].append(
                {"category": "Hate", "severity": response.hate_result.severity}
            )
        if response.self_harm_result:
            result["harm_analysis"].append(
                {"category": "SelfHarm", "severity": response.self_harm_result.severity}
            )
        if response.sexual_result:
            result["harm_analysis"].append(
                {"category": "Sexual", "severity": response.sexual_result.severity}
            )
        if response.violence_result:
            result["harm_analysis"].append(
                {"category": "Violence", "severity": response.violence_result.severity}
            )

        if response.blocklist_matches:
            for match in response.blocklist_matches:
                result["blocklist_matches"].append(
                    {
                        "blocklist_name": match.blocklist_name,
                        "block_item_text": match.block_item_text,
                        "block_item_id": match.block_item_id,
                    }
                )
        return result

    except Exception as e:
        return {"error": str(e)}
