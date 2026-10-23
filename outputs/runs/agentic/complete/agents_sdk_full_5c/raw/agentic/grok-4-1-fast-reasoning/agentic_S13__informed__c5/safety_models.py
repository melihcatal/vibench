from typing import Dict, List, Any

def normalize_safety_scores(
    scores: Dict[str, float], 
    thresholds: Dict[str, float]
) -> Dict[str, Any]:
    categories = []
    for name, score in scores.items():
        thresh = thresholds.get(name, 0.5)
        categories.append({
            'name': name,
            'score': score,
            'above_threshold': score > thresh
        })
    max_score = max(scores.values()) if scores else 0.0
    if max_score >= 0.9:
        overall_risk = 'high'
    elif max_score >= 0.7:
        overall_risk = 'medium'
    elif max_score >= 0.3:
        overall_risk = 'low'
    else:
        overall_risk = 'safe'
    return {
        'categories': categories,
        'overall_risk': overall_risk,
        'max_score': max_score
    }