from azure.ai.documentintelligence.models import AnalyzeResult

class DocumentModel:
    def __init__(self, analyze_result: AnalyzeResult):
        self.analyze_result = analyze_result