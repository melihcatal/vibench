from typing import Dict, List


class ModelRequest:
    def __init__(self, text: str):
        self.text = text


class ModelResponse:
    def __init__(self, text: str):
        self.text = text


def normalize_response(response: Dict) -> ModelResponse:
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return ModelResponse(text)