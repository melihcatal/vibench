from typing import Dict, Any, List

def apply_safety_thresholds(safety_ratings: List[Dict[str, Any]], thresholds: Dict[str, float]) -> Dict[str, Any]:
    allowed = True
    blocking_reasons = []
    probability_map = {
        'UNSPECIFIED': 0.0,
        'NEGLIGIBLE': 0.1,
        'LOW': 0.2,
        'MEDIUM': 0.5,
        'HIGH': 0.8,
        'VERY_HIGH': 0.9
    }

    for rating in safety_ratings:
        category = rating.get('category')
        probability_str = rating.get('probability')
        blocked_by_api = rating.get('blocked', False)

        if blocked_by_api:
            allowed = False
            blocking_reasons.append(f"Blocked by API for category: {category}")
            continue

        if category in thresholds:
            threshold_value = thresholds[category]
            numeric_probability = probability_map.get(probability_str, 0.0)

            if numeric_probability >= threshold_value:
                allowed = False
                blocking_reasons.append(f"Blocked by threshold for category: {category} (Score: {probability_str}, Threshold: {threshold_value})")

    return {
        "allowed": allowed,
        "blocking_reasons": blocking_reasons,
        "provider_context": "Google Vertex AI Safety Categories"
    }

