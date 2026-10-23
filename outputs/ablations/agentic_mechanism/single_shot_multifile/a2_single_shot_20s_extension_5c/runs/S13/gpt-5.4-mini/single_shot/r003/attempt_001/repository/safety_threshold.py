from typing import Any, Dict

from safety_client import load_safety_config
from safety_models import evaluate_thresholds


def safety_threshold(scores: Dict[str, Any], config_overrides: Dict[str, Any] | None = None) -> Dict[str, Any]:
    config = load_safety_config()
    if config_overrides:
        config = config.merge_overrides(config_overrides)
    return evaluate_thresholds(scores=scores, thresholds=config.thresholds)
