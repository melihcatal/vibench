from azure.ai.contentsafety.models import AnalyzeTextOptions


def create_analyze_options(text):
    return AnalyzeTextOptions(text=text, output_type='EightSeverityLevels')