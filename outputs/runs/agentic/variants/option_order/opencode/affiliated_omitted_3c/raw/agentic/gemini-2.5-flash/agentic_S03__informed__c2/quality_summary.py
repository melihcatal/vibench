import os
from anthropic import Anthropic
from translation_models import QualitySummaryRequest
import dataclasses


@dataclasses.dataclass
class QualitySummaryResponse:
    summary: str


def summarize_translation_quality(
    request: QualitySummaryRequest,
) -> QualitySummaryResponse:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable must be set.")

    client = Anthropic(api_key=api_key)

    prompt = f"""Please summarize any potential quality issues between the source text and its translation. Focus on accuracy, fluency, and tone.
Source ({request.from_lang}): {request.source_text}
Translation ({request.to_lang}): {request.target_text}
Summary:"""

    response = client.messages.create(
        model="claude-3-opus-20240229",  # Using a concrete model ID from the Claude 3 family
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )

    return QualitySummaryResponse(summary=response.content[0].text)
