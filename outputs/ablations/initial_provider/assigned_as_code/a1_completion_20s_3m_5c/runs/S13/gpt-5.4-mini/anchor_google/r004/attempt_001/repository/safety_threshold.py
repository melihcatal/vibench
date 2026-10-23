from safety_client import perspective_analyze, get_score, get_thresholds
from safety_models import normalize_text


def safety_threshold(payload, config=None):
    config = config or {}
    thresholds = get_thresholds(config)
    text = normalize_text(payload.get("text"))
    analysis = perspective_analyze(text, ["TOXICITY"], config=config)
    score = get_score(analysis, "TOXICITY")
    threshold = thresholds.get("TOXICITY", config.get("threshold", 0.5))
    return {"allow": score < threshold, "threshold": threshold, "toxicity": score}
