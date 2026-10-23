from .vision_client import get_vision_client


def normalize_response(response):
    return [label.name for label in response.labels]
