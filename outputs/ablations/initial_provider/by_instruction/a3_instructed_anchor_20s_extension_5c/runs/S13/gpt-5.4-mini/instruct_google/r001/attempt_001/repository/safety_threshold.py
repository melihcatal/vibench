from safety_client import get_threshold


def safety_threshold(categories):
    threshold = get_threshold()
    return all(float(score) < threshold for score in (categories or {}).values())
