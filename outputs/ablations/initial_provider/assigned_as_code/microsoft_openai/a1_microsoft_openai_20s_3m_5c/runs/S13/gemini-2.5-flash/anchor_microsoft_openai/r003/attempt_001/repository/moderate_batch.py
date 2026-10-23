from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_content_safety_client
from safety_models import ModerationResult, TextCategories

def moderate_batch(texts: list[str], config: dict) -> list[ModerationResult]:
    client = get_content_safety_client(config['endpoint'], config['api_key'])
    results = []
    for text in texts:
        response = client.analyze_text(AnalyzeTextOptions(text=text, output_type='EightSeverityLevels'))
        categories = {
            category.category: category.severity / 7
            for category in response.categories_analysis
        }
        is_unsafe = any(category.severity / 7 > config.get('default_batch_threshold', 0.5) for category in response.categories_analysis)
        results.append(ModerationResult(text=text, categories=categories, is_unsafe=is_unsafe))
    return results
