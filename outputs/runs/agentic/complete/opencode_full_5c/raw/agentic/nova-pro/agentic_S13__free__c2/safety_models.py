from typing import Dict, List


class SafetyRequest:
    def __init__(self, text: str):
        self.text = text


class SafetyResponse:
    def __init__(self, labels: Dict[str, float]):
        self.labels = labels


def normalize_response(response: Dict) -> SafetyResponse:
    labels = {label["Name"]: label["Score"] for label in response["Labels"]}
    return SafetyResponse(labels)
