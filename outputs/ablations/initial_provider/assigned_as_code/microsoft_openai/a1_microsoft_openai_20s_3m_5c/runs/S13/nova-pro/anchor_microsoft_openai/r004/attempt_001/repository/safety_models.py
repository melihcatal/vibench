from azure.ai.contentsafety.models import AnalyzeTextOptions

def create_analyze_text_options(text, output_type='EightSeverityLevels'):
    return AnalyzeTextOptions(text=text, output_type=output_type)

def normalize_response(response):
    return {'toxicity': max((category.severity for category in response.categories_analysis), default=0) / 7}