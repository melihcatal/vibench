from safety_client import safety_client
from safety_models import parse_redact_response
from azure.ai.contentsafety import AnalyzeAndRedactTextOptions, Category, RedactionMode

def redact_unsafe(text: str, threshold: str = "medium", mode: str = "mask") -> tuple[str, list[dict]]:
    request = AnalyzeAndRedactTextOptions(text=text)
    request.categories = [
        Category.HATE,
        Category.SEXUAL,
        Category.VIOLENCE,
        Category.SELFHARM
    ]
    request.redaction_mode = RedactionMode.MASK if mode == "mask" else RedactionMode.REMOVE
    request.block_threshold = threshold
    response = safety_client.analyze_and_redact_text(request)
    return parse_redact_response(response)
