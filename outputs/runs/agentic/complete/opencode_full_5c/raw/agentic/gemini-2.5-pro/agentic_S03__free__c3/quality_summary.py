from translation_client import anthropic_client
from translation_models import QualitySummaryRequest, QualitySummaryResponse


def quality_summary(request: QualitySummaryRequest) -> QualitySummaryResponse:
    """
    Summarizes translation quality issues using Anthropic Claude.
    """
    prompt = f"""Human: Review the following translation for quality.
Source Text: "{request.source_text}"
Translated Text: "{request.translated_text}"
Provide a brief summary of any potential issues, such as grammar, style, or incorrect meaning. If there are no issues, say so.

Assistant:"""

    message = anthropic_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    summary = message.content[0].text
    return QualitySummaryResponse(summary=summary)
