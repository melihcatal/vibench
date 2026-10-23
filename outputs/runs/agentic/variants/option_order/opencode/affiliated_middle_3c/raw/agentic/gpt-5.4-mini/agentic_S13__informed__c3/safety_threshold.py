from safety_client import SafetyClient


def safety_threshold(text: str, rules: dict[str, float]):
    return SafetyClient().safety_threshold(text, rules)
