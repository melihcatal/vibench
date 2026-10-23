from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_content_safety_client

def redact_unsafe(text: str, config: dict) -> str:
    client = get_content_safety_client(config['endpoint'], config['api_key'])
    response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
    
    # Determine if the text is unsafe based on a configured threshold
    is_unsafe = any(category.severity / 7 > config.get('redaction_threshold', 0.5) for category in response.categories_analysis)

    if is_unsafe:
        return "[REDACTED]"
    return text
