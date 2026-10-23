from safety_client import score_messages


def moderate_batch(messages, categories=None, thresholds=None):
    return score_messages(messages, categories=categories, thresholds=thresholds)
