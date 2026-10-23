from azure.ai.textanalytics import AnalyzeSentimentResult

def normalize_result(result):
    return {
        'sentiment': result.sentiment,
        'confidence_scores': result.confidence_scores
    }