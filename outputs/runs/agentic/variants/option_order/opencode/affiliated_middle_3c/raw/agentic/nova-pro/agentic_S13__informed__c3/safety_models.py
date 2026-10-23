from azure.ai.contentsafety.models import AnalyzeTextOptions, AnalyzeTextResult


class SafetyModels:
    @staticmethod
    def create_analyze_options(text):
        return AnalyzeTextOptions(text=text)

    @staticmethod
    def parse_analyze_result(result):
        return result
