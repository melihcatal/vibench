from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

from safety_client import get_safety_config, get_text
from safety_models import normalize_thresholds


def safety_threshold(payload, config=None):
    config = get_safety_config(config)
    thresholds = normalize_thresholds((config or {}).get('thresholds'))
    text = get_text(payload)
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
    categories = {}
    allow = True
    for item in getattr(response, 'categories_analysis', []) or []:
        name = str(getattr(item, 'category', 'unknown'))
        severity = getattr(item, 'severity', 0) / 7
        categories[name] = severity
        if severity >= thresholds.get(name, 0.5):
            allow = False
    return {'allow': allow, 'categories': categories}
