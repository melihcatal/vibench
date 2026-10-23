from.safety_client import get_content_safety_client


def normalize_response(response):
    return {'toxicity': max((category.severity for category in response.categories_analysis), default=0) / 7}


def build_analyze_text_options(text):
    from azure.ai.contentsafety.models import AnalyzeTextOptions
    return AnalyzeTextOptions(text=text, output_type='EightSeverityLevels')