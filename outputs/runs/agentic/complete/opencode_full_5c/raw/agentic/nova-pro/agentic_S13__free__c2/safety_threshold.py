from safety_models import SafetyResponse


def safety_threshold(response: SafetyResponse, thresholds: Dict[str, float]) -> bool:
    for label, score in response.labels.items():
        if score > thresholds.get(label, 0):
            return False
    return True
