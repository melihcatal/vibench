import json
import requests
from safety_client import (
    AWS_COMPREHEND_ENDPOINT,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)
from safety_models import SafetyRequest, SafetyResponse, normalize_response


def moderate_batch(texts: List[str]) -> List[SafetyResponse]:
    responses = []
    for text in texts:
        response = moderate_text(text)
        responses.append(response)
    return responses
