from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextCategory,
    AnalyzeTextOutputType,
)
from safety_client import get_content_safety_client
from safety_models import format_redaction_result


def redact_unsafe(text: str):
    client = get_content_safety_client()

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SEXUAL,
            TextCategory.SELF_HARM,
            TextCategory.VIOLENCE,
        ],
        output_type=AnalyzeTextOutputType.ANONYMIZED,
    )

    try:
        response = client.analyze_text(request)
        return format_redaction_result(response.redacted_text)
    except Exception as e:
        return {"error": str(e)}
