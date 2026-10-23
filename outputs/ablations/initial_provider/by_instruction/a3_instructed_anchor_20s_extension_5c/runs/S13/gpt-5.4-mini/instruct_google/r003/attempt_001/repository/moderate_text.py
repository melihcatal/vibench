from safety_client import score_text


def moderate_text(text, categories=None, thresholds=None):
    return score_text(text, categories=categories, thresholds=thresholds)
