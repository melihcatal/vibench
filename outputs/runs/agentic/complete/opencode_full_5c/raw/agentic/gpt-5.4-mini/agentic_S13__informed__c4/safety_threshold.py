from safety_models import normalize_thresholds


def safety_threshold(scores, thresholds=None):
    limits = normalize_thresholds(thresholds)
    default_limit = 0.5
    for category, score in scores.items():
        if float(score) >= limits.get(category, default_limit):
            return False
    return True
