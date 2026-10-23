from azure.ai.contentsafety.models import AnalyzeTextOptions

def create_analyze_text_options(text):
    return AnalyzeTextOptions(text=text)