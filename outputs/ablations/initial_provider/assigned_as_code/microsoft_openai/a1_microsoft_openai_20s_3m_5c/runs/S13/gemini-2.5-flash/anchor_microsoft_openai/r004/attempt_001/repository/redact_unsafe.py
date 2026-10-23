from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_azure_content_safety_client
from safety_models import RedactRequest, RedactResponse


def redact_unsafe(payload: RedactRequest, config=None) -> RedactResponse:
    client = get_azure_content_safety_client(config)
    response = client.analyze_text(AnalyzeTextOptions(text=payload.text, output_type='EightSeverityLevels', blocklist_names=[]))

    redacted_text = payload.text
    is_unsafe = False

    if response.harm_sentence_analysis is not None:
        for sentence in response.harm_sentence_analysis:
            if sentence.blocklists_match is not None:
                for block_match in sentence.blocklists_match:
                    for match_text in block_match.matching_text:
                        redacted_text = redacted_text.replace(match_text, "[REDACTED]")
                        is_unsafe = True

    for category_analysis in response.categories_analysis:
        if category_analysis.severity > 0:
            is_unsafe = True
            break

    return RedactResponse(redacted_text=redacted_text, is_unsafe=is_unsafe)
