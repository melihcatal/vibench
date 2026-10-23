from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_content_safety_client
from safety_models import format_moderation_result


def moderate_text(text: str):
    client = get_content_safety_client()

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SEXUAL,
            TextCategory.SELF_HARM,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
        return format_moderation_result(text, response)
    except Exception as e:
        return {"error": str(e)}
