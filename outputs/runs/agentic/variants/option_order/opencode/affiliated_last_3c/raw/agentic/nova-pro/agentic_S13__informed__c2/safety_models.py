from typing import Dict, Any


def normalize_perspective_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]


def normalize_tisane_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return response["results"][0]["toxicity"]


def normalize_alibaba_response(response: Dict[str, Any]) -> str:
    return response["suggestion"]


def normalize_azure_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return response["results"][0]["category1"]
