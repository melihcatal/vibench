from typing import Any, Dict

def normalize_sentiment_result(result: Any) -> Dict:
    return {
        'sentiment': result.sentiment,
        'positive_score': result.confidence_scores.positive,
        'neutral_score': result.confidence_scores.neutral,
        'negative_score': result.confidence_scores.negative,
    }