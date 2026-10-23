from safety_client import AzureContentSafetyClient
from safety_models import SafetyThresholdConfig, normalize_score_map, normalize_text


def safety_threshold(text: str, config: SafetyThresholdConfig) -> bool:
    client = AzureContentSafetyClient()
    raw = client.post("/contentsafety/text:analyze?api-version=2024-09-01", {"text": normalize_text(text)})
    categories = normalize_score_map(raw.get("categoriesAnalysis", {}))
    for category, threshold in config.thresholds.items():
        if categories.get(category, 0.0) >= threshold:
            return False
    return config.default_allow
