from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_content_safety_client
from safety_models import format_moderation_result


def moderate_batch(texts: list[str]):
    client = get_content_safety_client()
    results = []

    for text in texts:
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
            results.append(format_moderation_result(text, response))
        except Exception as e:
            results.append({"text": text, "error": str(e)})

    return results
