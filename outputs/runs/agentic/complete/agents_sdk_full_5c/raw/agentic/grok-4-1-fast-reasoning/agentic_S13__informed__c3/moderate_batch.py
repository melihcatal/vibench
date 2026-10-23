from safety_client import safety_client
from safety_models import ModerationResult, parse_analysis_response
from azure.ai.contentsafety import AnalyzeTextBatchOptions, Category
from azure.core.polling import LroPoller

def moderate_batch(texts: list[str]) -> list[ModerationResult]:
    analyses = []
    for text in texts:
        request = AnalyzeTextOptions(text=text)
        request.categories = [
            Category.HATE,
            Category.SEXUAL,
            Category.VIOLENCE,
            Category.SELFHARM
        ]
        analyses.append(request)
    poller: LroPoller = safety_client.begin_analyze_text_batch(analyses=analyses)
    result = poller.result()
    return [parse_analysis_response(analysis) for analysis in result]
