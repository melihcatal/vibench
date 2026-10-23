from safety_client import safety_client
from safety_models import ModerationResult, parse_analysis_response
from azure.ai.contentsafety import AnalyzeTextOptions, Category

def moderate_text(text: str) -> ModerationResult:
    request = AnalyzeTextOptions(text=text)
    request.categories = [
        Category.HATE,
        Category.SEXUAL,
        Category.VIOLENCE,
        Category.SELFHARM
    ]
    response = safety_client.analyze_text(request)
    return parse_analysis_response(response)
