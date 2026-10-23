from typing import Dict


def normalize_response(response: Dict):
    return response["completion"]


def parse_response(response):
    return response.completion
