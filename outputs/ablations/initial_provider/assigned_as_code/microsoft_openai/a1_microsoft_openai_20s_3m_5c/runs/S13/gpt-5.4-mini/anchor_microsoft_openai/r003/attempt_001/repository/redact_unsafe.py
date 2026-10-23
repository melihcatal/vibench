from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

from safety_client import get_safety_config, get_text


def redact_unsafe(payload, config=None):
    config = get_safety_config(config)
    text = get_text(payload)
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
    redacted = text
    unsafe = False
    for category in getattr(response, 'categories_analysis', []) or []:
        if getattr(category, 'severity', 0) >= 4:
            unsafe = True
            redacted = redacted.replace(text, '[REDACTED]')
            break
    return {'text': redacted, 'unsafe': unsafe}
