from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

from safety_client import get_safety_config, get_texts, severity_score
from safety_models import build_message_result


def moderate_batch(payload, config=None):
    config = get_safety_config(config)
    texts = get_texts(payload)
    results = []
    with ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        for text in texts:
            response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
            score = max((severity_score(category) for category in response.categories_analysis), default=0)
            results.append(build_message_result(text, 'block' if score >= 0.5 else 'allow', score))
    return {'results': results}
